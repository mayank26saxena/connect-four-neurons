"""Assemble the neuron atlas page data: copy results/atlas/* and a reduced tactics.json into docs/blog/atlas/data/, with
integrity checks (every layer has all neurons, both poles, examples that exist in games.json). Stdlib only."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, RES, DST = ROOT / "results" / "atlas", ROOT / "results", ROOT / "docs" / "blog" / "atlas" / "data"


def main():
    DST.mkdir(parents=True, exist_ok=True)
    meta = json.loads((SRC / "meta.json").read_text())
    games = json.loads((SRC / "games.json").read_text())
    L, Fd = meta["config"]["n_layer"], meta["config"]["d_ff"]
    n_ex = 0
    for l in range(L):
        recs = json.loads((SRC / f"L{l}.json").read_text())
        assert len(recs) == Fd, (l, len(recs))
        for r in recs:
            assert len(r["poles"]) == 2 and all(p is not None for p in r["poles"]) and len(r["dle"]) == 7 and len(r["tac"]) == len(meta["tactics"])
            for p in r["poles"]:
                assert len(p["occ"]) == 126 and len(p["F1"]) == 3
                for g, t, a in p["ex"]:
                    assert str(g) in games and 0 <= t <= len(games[str(g)]), (l, r["n"], g, t)
                    n_ex += 1
    ov = json.loads((SRC / "overview.json").read_text())
    assert len(ov["layer"]) == 2 * L * Fd and len(ov["c"]) == len(ov["layer"])
    for f in ["meta.json", "games.json", "overview.json"] + [f"L{l}.json" for l in range(L)]:
        shutil.copy(SRC / f, DST / f)
    a = json.loads((RES / "tactic_atlas.json").read_text())
    e = json.loads((RES / "tactic_emergence.json").read_text())
    keep = ("tactics", "columns", "n_positions", "chance", "intact", "components", "component_drop", "top_neurons", "neuron_validation", "probe_auroc", "probe_base_rate")
    (DST / "tactics.json").write_text(json.dumps({**{k: a[k] for k in keep}, "emergence": e}, separators=(",", ":")))
    print(f"atlas data ok: {L * Fd} neurons, {n_ex} examples checked, {len(games)} games")


if __name__ == "__main__":
    main()
