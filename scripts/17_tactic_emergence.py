"""When does each tactic appear, and when do its components specialise? For each checkpoint: the rate of every tactic and the
control, and the drop (mean-ablation) of the components that were tactic-specific in the final model. Needs
results/tactic_atlas.json from 16_tactic_atlas.py. Writes tactic_emergence.json."""
import json

import torch

from c4n import config, provenance
from c4n import tactics as T
from c4n.data import load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, TC = CFG["analysis"], CFG["tactics"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def main():
    atlas = json.loads((config.results_dir(CFG) / "tactic_atlas.json").read_text())
    comps, drop, cols = atlas["components"], atlas["component_drop"], atlas["columns"]
    key = []  # components with tactic-specific damage (tactic drop minus control drop) above 2 points for some tactic, plus every MLP
    for i, (c, d) in enumerate(zip(comps, drop)):
        if c["kind"] == "mlp" or max(d[j] - d[-1] for j in range(len(cols) - 1)) > 0.02:
            key.append(i)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    sets = T.tactic_sets(moves, lengths, TC["max_positions"], CFG["seed"])
    sets["control"] = T.control_set(moves, lengths, scores, TC["max_positions"], CFG["seed"])
    ck_dir = config.ROOT / CFG["train"]["out_dir"]
    out = {"columns": cols, "components": [comps[i] for i in key], "steps": [], "intact": [], "component_drop": []}
    for step in TC["emergence_ckpts"]:
        model = load_checkpoint(ck_dir / f"step_{step:06d}.pt", DEV)
        mean_a, mean_y = T.means(model, moves, lengths, DEV)
        intact = {t: T.rate(model, moves, sets[t], DEV) for t in cols}
        rows = []
        for i in key:
            c = comps[i]
            kw = {"hook": T.mlp_mean_hook(c["layer"], mean_a)} if c["kind"] == "mlp" else {"attn_hook": T.head_mean_hook(c["layer"], c["head"], mean_y)}
            rows.append([intact[t] - T.rate(model, moves, sets[t], DEV, **kw) for t in cols])
        out["steps"].append(step); out["intact"].append([intact[t] for t in cols]); out["component_drop"].append(rows)
        print(step, {t: round(v, 3) for t, v in intact.items()}, flush=True)
    path = config.results_dir(CFG) / "tactic_emergence.json"
    path.write_text(json.dumps(out))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
