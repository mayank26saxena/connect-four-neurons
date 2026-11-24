"""Neuron Scientist atlas: data for docs/blog/ns-atlas/ from the finished studies (q) and (r) (PLAN.md addenda q, r).

Reads only final artefacts: ns/report.json, ns2/report.json, ns{,2}/descriptions/*.json (results are not re-scored), and the
existing neuron-atlas data (docs/blog/atlas/data/L*.json, games.json) and the post-hoc opening label (ns/opening_label.json) for each real neuron's top-firing dev positions. Random
directions are shown with the positions the describing agent built for them (their directions live in the answer keys, which are
not used). Writes docs/blog/ns-atlas/data/ns.js (window.NS = {...}). Light work on JSON files; no model is run.
Checks: the number of real units with held-out F1 >= 0.5 per study must match docs/NS_RESULTS.md (25 in q, 19 in r, 44 in all)."""
import json
import math
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "docs" / "blog" / "atlas" / "data"
OUT = ROOT / "docs" / "blog" / "ns-atlas" / "data"
BAR = 0.5                 # the atlas bar set in docs/NS_RESULTS.md after the studies (not pre-registered)
EXPECTED = {"q": 25, "r": 19}


def fnum(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 4)


def med(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return round(st.median(xs), 4) if xs else None


def main():
    layers = {l: json.loads((ATLAS / f"L{l}.json").read_text()) for l in range(6)}
    games = json.loads((ATLAS / "games.json").read_text())
    opening = json.loads((ROOT / "ns" / "opening_label.json").read_text())  # post-hoc label, scripts/34_ns_opening_label.py
    units, studies = [], {}
    for study, ws in (("q", "ns"), ("r", "ns2")):
        rep = json.loads((ROOT / ws / "report.json").read_text())
        judge = rep.get("judge") or {}
        per = judge.get("per_unit", {})
        rows = rep["rows"]
        for r in rows:
            d = json.loads((ROOT / ws / "descriptions" / f"{r['unit']}.json").read_text())
            real = r["kind"] == "neuron"
            cat = ("verified" if r["test_f1"] >= BAR else "below") if real else "control"
            ex = []
            if real:
                pole = next(p for p in layers[r["layer"]][r["neuron"]]["poles"] if p["s"] == r["pole"])
                for g, t, a in pole["ex"][:4]:
                    ex.append({"moves": [int(c) for c in games[str(g)][:t]], "act": a})
            n_pairs = len(json.loads((ROOT / ws / "judge" / f"{r['unit']}.json").read_text())["pairs"])
            units.append({
                "id": f"{study}-{r['unit']}", "study": study, "unit": r["unit"], "kind": r["kind"], "stratum": r["stratum"], "cat": cat,
                "layer": r["layer"], "neuron": r["neuron"], "pole": r["pole"], "confidence": r["confidence"],
                "description": d["description"], "effect": d.get("effect", ""), "program": d["program"], "notes": d.get("notes", ""),
                "f1": fnum(r["test_f1"]), "precision": fnum(r["test_precision"]), "recall": fnum(r["test_recall"]), "auroc": fnum(r["test_auroc"]),
                "dict_concept": r["dict_concept"], "dict_f1": fnum(r["dict_test_f1"]), "judge": fnum(per.get(r["unit"])), "judge_pairs": n_pairs,
                "sim_share": fnum(r["sim_share"]), "synth_beats": bool(r["synthesis_beats_max"]), "synth_best": fnum(r["synthesis_best"]),
                "dev_max": fnum(r["dev_max"]), "synthesis": d["synthesis"][:3], "steer": [round(x, 3) for x in r["steer_effect"]],
                "examples": ex, "dev_calls": r.get("dev_calls_used"),
                "opening": opening["units"].get(f"{study}-{r['unit']}", {}).get("opening", False),
                "early_share": opening["units"].get(f"{study}-{r['unit']}", {}).get("early_share")})
        real = [u for u in units if u["study"] == study and u["kind"] == "neuron"]
        n_ok = sum(u["cat"] == "verified" for u in real)
        assert n_ok == EXPECTED[study], f"study {study}: {n_ok} real units at F1 >= {BAR}, NS_RESULTS.md says {EXPECTED[study]}"
        strata = {}
        for s in ("explained", "unexplained", "random"):
            us = [u for u in units if u["study"] == study and u["stratum"] == s]
            strata[s] = {"n": len(us), "f1": med([u["f1"] for u in us]), "dict": med([u["dict_f1"] for u in us]),
                         "judge": med([u["judge"] for u in us]), "low": round(sum(u["confidence"] == "low" for u in us) / len(us), 3),
                         "n_f1_ge_bar": sum((u["f1"] or 0) >= BAR for u in us)}
        preds = {k: v for k, v in rep["summary"]["predictions"].items()}
        preds["q_e"] = {"real_mean": judge.get("real_mean"), "random_mean": judge.get("random_mean"), "holds": judge.get("q_e_holds")}
        studies[study] = {"n_units": len(rows), "n_real": len(real), "n_verified": n_ok, "strata": strata,
                          "predictions": json.loads(json.dumps(preds, default=str).replace("NaN", "null"))}
    ctrl = [u for u in units if u["kind"] != "neuron"]
    out = {"bar": BAR, "studies": studies, "units": units,
           "totals": {"real": sum(u["kind"] == "neuron" for u in units), "verified": sum(u["cat"] == "verified" for u in units),
                      "controls": len(ctrl), "controls_ge_bar": sum((u["f1"] or 0) >= BAR for u in ctrl),
                      "best_control": max(ctrl, key=lambda u: u["f1"] or 0)["id"],
                      "verified_opening": sum(u["cat"] == "verified" and u["opening"] for u in units),
                      "controls_ge_bar_opening": sum((u["f1"] or 0) >= BAR and u["opening"] for u in ctrl)},
           "opening_rule": opening["rule"]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ns.js").write_text("window.NS = " + json.dumps(out, allow_nan=False) + ";\n")
    t = out["totals"]
    print(f"{len(units)} units: {t['real']} real ({t['verified']} at F1 >= {BAR}), {t['controls']} random-direction controls "
          f"({t['controls_ge_bar']} at F1 >= {BAR}); wrote {OUT / 'ns.js'}")


if __name__ == "__main__":
    main()
