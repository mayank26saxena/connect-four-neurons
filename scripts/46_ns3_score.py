"""Test B scoring (PLAN.md addendum (s), S7). Run only after every ns3 description is frozen (returned 2026-11-23, zip sha256
5f8c3658...) and after `C4N_CONFIG=ns3 NS_DIR=ns3 python scripts/32_ns_verify.py run` (the (r) verification, unchanged).
Measures, validation split (first n_games games), positions with >= 4 stones:
  - tactic agreement (as in S6, scripts/36): best F1 of the frozen program's firing against block_now_c0-c6 and block_now_any;
  - held-out F1 against the unit's own firing at the primary threshold (dev p97 / p3, from ns3/stats.json), and at p90 / p80
    (secondary; thresholds taken the same way, over eligible dev positions; frozen programs, no agent re-run);
  - the text-only check (s-B2) from ns3/textcheck/scored.json if present (scripts/45_ns3_textcheck.py), else marked pending.
Then unblinds with results/ns3_membership.json and tests s-B1, s-B2, s-B3; s-B4 (random directions) is reported as in (r).
A follow-up (labelled, not registered): the same numbers without the 13 units the orchestrator logged as breaking the rule against
local evaluation. Writes results/ns3_testB.json. Run with C4N_CONFIG=ns3 NS_DIR=ns3 on a GPU host."""
import json

import numpy as np

from c4n import circuit as C
from c4n import config, ns, provenance

CFG = config.load()
NC = ns.ns_config(CFG)
ROOT = config.ROOT
OUT = ROOT / "results" / "ns3_testB.json"
RULE_BREAKS = ["U02", "U08", "U16", "U21", "U23", "U26", "U27", "U30", "U32", "U37", "U45", "U48", "U50"]  # ns3/orchestrator_log.md
PCTS = {"p97": 97, "p90": 90, "p80": 80}


def boot(a, b, fn, n=2000, seed=0):
    """95% interval of fn(a, b) with a and b resampled independently (unit-level bootstrap)."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    v = [fn(a[rng.integers(0, len(a), len(a))], b[rng.integers(0, len(b), len(b))]) for _ in range(n)]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def summary(rows, label):
    g = lambda name: [r for r in rows if r["group"] == name]
    circ, dec, rnd = g("circuit"), g("decoy"), g("random")
    out = {"label": label, "n": {"circuit": len(circ), "decoy": len(dec), "random": len(rnd)}}
    ta = lambda rs: [r["tactic_agreement"] >= 0.5 for r in rs]
    out["s_B1"] = {"circuit_share_ge_0.5": float(np.mean(ta(circ))), "decoy_share_ge_0.5": float(np.mean(ta(dec))),
                   "random_share_ge_0.5": float(np.mean(ta(rnd))) if rnd else None,
                   "holds": bool(np.mean(ta(circ)) >= 0.5 and np.mean(ta(dec)) <= 0.10)}
    if all(r["textcheck_yes"] is not None for r in circ + dec):
        yc, yd = np.mean([r["textcheck_yes"] for r in circ]), np.mean([r["textcheck_yes"] for r in dec])
        out["s_B2"] = {"circuit_yes": float(yc), "decoy_yes": float(yd), "holds": bool(yc >= 0.5 and yd <= 0.10)}
    else:
        out["s_B2"] = {"pending": "text-only check not yet run (scripts/45_ns3_textcheck.py, separate account)"}
    for k in PCTS:
        fc, fd = [r[f"f1_{k}"] for r in circ], [r[f"f1_{k}"] for r in dec]
        d = float(np.median(fc) - np.median(fd))
        ent = {"circuit_median": float(np.median(fc)), "decoy_median": float(np.median(fd)), "diff": d,
               "ci95": boot(fc, fd, lambda a, b: np.median(a) - np.median(b))}
        if k == "p97":
            ent["holds"] = d >= 0.10
            out["s_B3"] = ent
        else:
            out[f"s_B3_{k}_secondary"] = ent
    if rnd:
        real = [r["f1_p97"] for r in circ + dec]
        p90 = float(np.percentile([r["f1_p97"] for r in rnd], 90))
        out["s_B4"] = {"real_median_f1": float(np.median(real)), "random_median_f1": float(np.median([r["f1_p97"] for r in rnd])),
                       "real_minus_random": float(np.median(real) - np.median([r["f1_p97"] for r in rnd])), "random_f1_p90": p90,
                       "real_frac_above_random_p90": float(np.mean([x > p90 for x in real])), "for_comparability_only": True}
    out["confidence"] = {grp: {c: int(sum(r["confidence"] == c for r in g(grp))) for c in ("high", "medium", "low")} for grp in ("circuit", "decoy", "random")}
    return out


def main():
    key, st = ns.unit_key(), ns.stats()
    memb = json.loads((ROOT / "results" / "ns3_membership.json").read_text())["units"]
    rep = {r["unit"]: r for r in json.loads((ns.NS / "report.json").read_text())["rows"]}
    tc_path = ns.NS / "textcheck" / "scored.json"
    tc = json.loads(tc_path.read_text())["yes"] if tc_path.exists() else {}
    units = sorted(p.stem for p in (ns.NS / "descriptions").glob("U*.json"))
    assert len(units) == 50 and set(units) == set(memb), "every unit must have a frozen description"
    dmoves, _, dlen = ns.load_games(ns.DEV_SPLIT, NC["n_games"])
    tmoves, _, tlen = ns.load_games(ns.TEST_SPLIT, NC["n_games"])
    allu = [u["id"] for u in ns.units()]
    S_dev = np.load(ns.CACHE / "dev_acts.npy")[:, [allu.index(u) for u in units]]
    S_test = np.load(ns.CACHE / "test_acts.npy")[:, [allu.index(u) for u in units]]  # written by 32_ns_verify.py run
    el_dev, el_test = ns.eligible(dlen, NC["min_ply"]), ns.eligible(tlen, NC["min_ply"])
    bs = ns.BoardSet(tmoves, tlen)
    _, _, block, _ = C.facts(bs.pos, bs.mask)
    conc = {f"block_now_c{c}": block[:, c] for c in range(7)}
    conc["block_now_any"] = block.any(1)
    rows = []
    for j, u in enumerate(units):
        d = json.loads((ns.NS / "descriptions" / f"{u}.json").read_text())
        fires_fn, _ = ns.load_program(d["program"])
        pred = ns.run_program(fires_fn, bs) >= 0.5
        sc = {k: ns.f1(pred[el_test], v[el_test])[0] for k, v in conc.items()}
        best = max(sc, key=sc.get)
        sign = st[u]["sign"]
        f1s, thr = {}, {}
        for k, q in PCTS.items():
            t = np.percentile(sign * S_dev[el_dev, j], q)
            thr[k] = float(sign * t)
            fire = sign * S_test[:, j] > t
            f1s[k] = float(ns.f1(pred[el_test], fire[el_test])[0])
        f_primary = ns.fires_from(S_test[:, j], st, u)
        f1_primary = float(ns.f1(pred[el_test], f_primary[el_test])[0])
        k_ = key[u]
        rows.append({"unit": u, "group": memb[u]["group"], "rank": memb[u].get("rank"), "exact_effect": memb[u].get("exact_effect"),
                     "layer": k_["layer"], "neuron": k_.get("neuron"), "pole": "+" if sign > 0 else "-",
                     "tactic_agreement": float(sc[best]), "best_block_concept": best, "tactic_scores": {k: float(v) for k, v in sc.items()},
                     "program_fire_rate": float(pred[el_test].mean()), "f1_p97": f1_primary, "f1_p97_recomputed_pct": f1s["p97"],
                     "f1_p90": f1s["p90"], "f1_p80": f1s["p80"], "thr": thr, "stats_thr_p97": st[u]["thr"],
                     "verify_test_f1": rep[u]["test_f1"], "verify_auroc": rep[u]["test_auroc"], "sim_share": rep[u]["sim_share"],
                     "synthesis_beats_max": rep[u]["synthesis_beats_max"], "textcheck_yes": tc.get(u), "confidence": d["confidence"],
                     "rule_break": u in RULE_BREAKS, "description": d["description"], "effect": d.get("effect", "")})
        print(f"{u} {memb[u]['group']:7} L{k_['layer']} tactic {sc[best]:.2f} ({best}) F1 p97 {f1_primary:.2f} p90 {f1s['p90']:.2f} "
              f"p80 {f1s['p80']:.2f} conf {d['confidence']}", flush=True)
    bad = [r["unit"] for r in rows if abs(r["f1_p97"] - r["verify_test_f1"]) > 1e-9]
    assert not bad, f"own-firing F1 differs from 32_ns_verify for {bad}"
    out = {"study": "(s) Test B, PLAN.md S7", "n_val_games": NC["n_games"], "min_ply": NC["min_ply"],
           "primary": summary(rows, "all 50 units (registered)"),
           "followup_excluding_rule_breaks": summary([r for r in rows if not r["rule_break"]],
                                                     "follow-up, not registered: excluding the 13 logged rule breaks"),
           "rule_breaks": RULE_BREAKS, "rows": rows}
    OUT.write_text(json.dumps(out, indent=1))
    provenance.write(OUT, {"n_games": NC["n_games"]})
    print(json.dumps({k: v for k, v in out["primary"].items()}, indent=1))
    print(json.dumps(out["followup_excluding_rule_breaks"], indent=1))


if __name__ == "__main__":
    main()
