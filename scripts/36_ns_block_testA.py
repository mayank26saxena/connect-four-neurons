"""Test A (PLAN.md addendum (s), S6): do the existing (q)/(r) descriptions point at the frozen blocking circuit?
A new analysis of frozen programs, labelled as a follow-up: no (q)/(r) result is re-scored or edited. Reads results/block_circuit.json
(frozen first, S5), ns/ and ns2/ reports and descriptions. Tactic agreement = best F1 of a frozen program's firing (>= 0.5) against
the ground-truth concepts block_now_c0-c6 and block_now_any, on validation positions with >= 4 stones (first `n_games` games).
Writes results/ns_block_testA.json."""
import json
import os

import numpy as np

from c4n import circuit as C
from c4n import config, ns, provenance

ROOT = config.ROOT
N_GAMES = int(os.environ.get("TESTA_GAMES", 2000))
OUT = ROOT / "results" / "ns_block_testA.json"


def block_concepts(bs):
    _, _, block, _ = C.facts(bs.pos, bs.mask)
    out = {f"block_now_c{c}": block[:, c] for c in range(7)}
    out["block_now_any"] = block.any(1)
    return out


def tactic_agreement(program, bs, el, conc):
    fires, _ = ns.load_program(program)
    pred = ns.run_program(fires, bs) >= 0.5
    scores = {k: ns.f1(pred[el], v[el])[0] for k, v in conc.items()}
    best = max(scores, key=scores.get)
    return float(scores[best]), best, float(pred[el].mean())


def main():
    circ = json.loads((ROOT / "results" / "block_circuit.json").read_text())
    cpoles = {(n["layer"], n["neuron"], n["pole"]): n for n in circ["circuit"]["neurons"]}
    cneur = {(n["layer"], n["neuron"]) for n in circ["circuit"]["neurons"]}
    rank = {(r["layer"], r["neuron"]): i for i, r in enumerate(circ["circuit"]["ranked_top"])}
    Fd = 1024
    attr_rank = {(f // Fd, f % Fd): i for i, f in enumerate(circ["circuit"]["attr_rank_top1000"])}
    moves, _, lengths = ns.load_games(ns.TEST_SPLIT, N_GAMES)
    bs = ns.BoardSet(moves, lengths)
    el = ns.eligible(lengths, 4)
    conc = block_concepts(bs)
    rows = []
    for study, ws in (("q", "ns"), ("r", "ns2")):
        rep = json.loads((ROOT / ws / "report.json").read_text())
        for r in rep["rows"]:
            if r["kind"] != "neuron":
                continue
            d = json.loads((ROOT / ws / "descriptions" / f"{r['unit']}.json").read_text())
            ta, best, rate = tactic_agreement(d["program"], bs, el, conc)
            key = (r["layer"], r["neuron"])
            rows.append({"id": f"{study}-{r['unit']}", "layer": r["layer"], "neuron": r["neuron"], "pole": r["pole"],
                         "test_f1_reported": r["test_f1"], "tactic_agreement": ta, "best_block_concept": best, "program_fire_rate": rate,
                         "in_circuit_pole": (r["layer"], r["neuron"], r["pole"]) in cpoles, "in_circuit_neuron": key in cneur,
                         "exact_rank": rank.get(key), "attr_rank": attr_rank.get(key), "description": d["description"]})
    n_c = len(circ["circuit"]["neurons"])
    overlap = [x for x in rows if x["in_circuit_neuron"]]
    tact = sorted([x for x in rows if x["tactic_agreement"] >= 0.5], key=lambda x: -x["tactic_agreement"])
    out = {"followup": "PLAN (s) S6; frozen (q)/(r) programs, not re-scored", "n_val_games": N_GAMES, "circuit_size": n_c,
           "circuit_compact": circ["circuit"]["compact"], "n_real_units": len(rows),
           "expected_overlap_by_chance_poles": n_c * len(rows) / 12288,
           "overlap": overlap, "units_with_tactic_agreement_ge_0.5": tact, "all": rows}
    OUT.write_text(json.dumps(out, indent=1))
    provenance.write(OUT, {"n_games": N_GAMES})
    print(f"circuit {n_c} neurons; {len(overlap)} of {len(rows)} described real units are circuit neurons "
          f"(chance {out['expected_overlap_by_chance_poles']:.2f} poles); {len(tact)} units have tactic agreement >= 0.5")
    for x in tact:
        print(f"  {x['id']} L{x['layer']}N{x['neuron']}{x['pole']} agree {x['tactic_agreement']:.2f} ({x['best_block_concept']}) "
              f"exact_rank {x['exact_rank']} attr_rank {x['attr_rank']} circuit {x['in_circuit_neuron']}")


if __name__ == "__main__":
    main()
