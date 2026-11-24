"""Neuron Scientist, step 3: held-out verification (PLAN.md addendum (q)). Run only after every description is frozen.

  run            score every ns/descriptions/*.json on the test split (validation games): exact detection, simulation share of
                 ceiling, input synthesis, measured steering effect; dictionary baseline; unblinded summary -> ns/report.json/.md
  judge-export   text-only detection packs: for each unit, judge_pairs pairs of boards (one fires, one does not), order shuffled;
                 written to ns/judge/<unit>.json (description text + pairs only); answer key to ns/private/judge_key.json
  judge-score    read ns/judge_answers/<unit>.json ({"answers": ["A", "B", ...]}) and add text-only detection to the report
"""
import argparse
import json

import numpy as np
import torch

from c4n import config
from c4n import ns
from c4n.concepts import NAMES
from c4n.data import concepts_for

CFG = config.load()
NC = ns.ns_config(CFG)


def load_descriptions():
    d = {}
    for f in sorted((ns.NS / "descriptions").glob("U*.json")):
        x = json.loads(f.read_text())
        d[x["unit"]] = x
    return d


def test_acts(model, us, key):
    path = ns.CACHE / "test_acts.npy"
    allu = [u["id"] for u in ns.units()]
    if path.exists():
        S = np.load(path)
    else:
        moves, _, lengths = ns.load_games(ns.TEST_SPLIT, NC["n_games"])
        S = ns.unit_acts(model, moves, lengths, allu, key).astype(np.float32)
        np.save(path, S)
    return S[:, [allu.index(u) for u in us]]


def boot_median_diff(a, b, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a), np.asarray(b)
    d = [np.median(a[i] - b[i]) for i in (rng.integers(0, len(a), len(a)) for _ in range(n))]
    return [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]


def cmd_run(a):
    desc = load_descriptions()
    key, st = ns.unit_key(), ns.stats()
    us = sorted(desc)
    model = ns.load_web_model()
    dmoves, dscores, dlen = ns.load_games(ns.DEV_SPLIT, NC["n_games"])
    tmoves, tscores, tlen = ns.load_games(ns.TEST_SPLIT, NC["n_games"])
    allu = [u["id"] for u in ns.units()]
    S_dev = np.load(ns.CACHE / "dev_acts.npy")[:, [allu.index(u) for u in us]]
    S_test = test_acts(model, us, key)
    dev_bs, test_bs = ns.BoardSet(dmoves, dlen), ns.BoardSet(tmoves, tlen)
    # dictionary baseline: best concept on dev, scored on test
    C_dev = concepts_for(CFG, ns.DEV_SPLIT, NC["n_games"]).astype(bool)
    C_test = concepts_for(CFG, ns.TEST_SPLIT, NC["n_games"]).astype(bool)
    fit_cut = int(dlen[:NC["fit_games"]].sum())
    sim_n = NC["test_sim_games"]
    sim_cut = int(tlen[:sim_n].sum())
    el_dev, el_test = ns.eligible(dlen, NC["min_ply"]), ns.eligible(tlen, NC["min_ply"])  # (r) eligible positions only
    rows = []
    for j, u in enumerate(us):
        d = desc[u]
        fires_fn, level_fn = ns.load_program(d["program"])
        f_dev, f_test = ns.fires_from(S_dev[:, j], st, u), ns.fires_from(S_test[:, j], st, u)
        pv = ns.run_program(fires_fn, test_bs)
        f1, prec, rec = ns.f1((pv >= 0.5)[el_test], f_test[el_test])
        au = ns.auroc(pv[el_test], f_test[el_test])
        # dictionary (chosen on eligible dev positions, scored on eligible test positions)
        Cd, fd = C_dev[el_dev], f_dev[el_dev]
        tp = (Cd & fd[:, None]).sum(0)
        dict_f1_dev = 2 * tp / np.maximum(1, Cd.sum(0) + fd.sum())
        k = int(np.argmax(dict_f1_dev))
        df1 = ns.f1(C_test[el_test, k], f_test[el_test])[0]
        # simulation: level map fitted on the first fit_games dev games, applied to the first test_sim_games test games
        lv_fit = ns.run_program(level_fn or fires_fn, dev_bs, range(fit_cut))
        m = ns.level_map(lv_fit, S_dev[:fit_cut, j])
        lv_test = ns.run_program(level_fn or fires_fn, test_bs, range(sim_cut))
        sim = ns.kl_recovery(model, tmoves[:sim_n], tlen[:sim_n], u, key, ns.apply_level_map(m, lv_test), S_test[:sim_cut, j])
        q = np.quantile(S_dev[:fit_cut, j], np.linspace(0, 1, 11)[1:-1])
        cm = ns.level_map(np.digitize(S_dev[:fit_cut, j], q), S_dev[:fit_cut, j])
        ceil = ns.kl_recovery(model, tmoves[:sim_n], tlen[:sim_n], u, key, ns.apply_level_map(cm, np.digitize(S_test[:sim_cut, j], q)), S_test[:sim_cut, j])
        share = sim["recovery"] / ceil["recovery"] if ceil["recovery"] > 0 else float("nan")
        # input synthesis
        syn = [st[u]["sign"] * ns.acts_for_sequence(model, s, u, key)[-1] for s in d["synthesis"] if len(s) >= NC["min_ply"]]
        syn_ok = bool(len(syn) and max(syn) > st[u]["dev_max_pole"])
        # measured steering effect: mean change in move probabilities when the unit is set to its dev max, 200 test positions
        rng = np.random.default_rng(j)
        eff = np.zeros(7)
        for i in rng.choice(len(test_bs), 200, replace=False):
            mv = test_bs.board(int(i)).moves
            eff += ns.move_probs(model, mv, u, key, st[u]["dev_max_raw"]) - ns.move_probs(model, mv)
        eff /= 200
        kk = key[u]
        rows.append({"unit": u, "kind": kk["kind"], "stratum": kk["stratum"], "layer": kk["layer"], "neuron": kk.get("neuron"),
                     "pole": "+" if kk["sign"] > 0 else "-", "confidence": d["confidence"], "description": d["description"],
                     "test_f1": f1, "test_precision": prec, "test_recall": rec, "test_auroc": au, "dict_concept": NAMES[k], "dict_test_f1": df1,
                     "sim_recovery": sim["recovery"], "ceiling_recovery": ceil["recovery"], "sim_share": share,
                     "synthesis_best": float(max(syn)) if syn else None, "dev_max": st[u]["dev_max_pole"], "synthesis_beats_max": syn_ok,
                     "steer_effect": eff.round(4).tolist(), "dev_calls_used": d.get("dev_calls_used")})
        print(f"{u} {kk['stratum']:11} F1 {f1:.2f} (dict {df1:.2f}) AUROC {au:.2f} sim {share:.2f} synth {'yes' if syn_ok else 'no'}  "
              f"conf {d['confidence']}", flush=True)
    rep = {"rows": rows, "summary": summarise(rows)}
    old = ns.NS / "report.json"
    if old.exists():
        rep["judge"] = json.loads(old.read_text()).get("judge")
    (ns.NS / "report.json").write_text(json.dumps(rep, indent=1))
    write_md(rep)
    print(json.dumps(rep["summary"], indent=1))


def summarise(rows):
    def med(xs):  # (r) NaN-safe: units with an undefined value are skipped (and counted in *_n_nan)
        if NC["study"] == "r":
            xs = [x for x in xs if x is not None and not np.isnan(x)]
        return float(np.median(xs)) if len(xs) else None
    by = lambda s: [r for r in rows if r["stratum"] == s]
    real = [r for r in rows if r["kind"] == "neuron"]
    out = {}
    for s in ("explained", "unexplained", "random"):
        rs = by(s)
        out[s] = {"n": len(rs), "agent_f1_median": med([r["test_f1"] for r in rs]), "dict_f1_median": med([r["dict_test_f1"] for r in rs]),
                  "auroc_median": med([r["test_auroc"] for r in rs]), "sim_share_median": med([r["sim_share"] for r in rs]),
                  "synthesis_rate": float(np.mean([r["synthesis_beats_max"] for r in rs])) if rs else None,
                  "low_confidence_rate": float(np.mean([r["confidence"] == "low" for r in rs])) if rs else None,
                  "sim_share_n_nan": int(sum(1 for r in rs if r["sim_share"] is None or np.isnan(r["sim_share"])))}
    ue, ex, rd = by("unexplained"), by("explained"), by("random")
    pred = {}
    if ue:
        diff = float(np.median([r["test_f1"] - r["dict_test_f1"] for r in ue]))
        pred["q_a"] = {"median_agent_minus_dict": diff, "ci95": boot_median_diff([r["test_f1"] for r in ue], [r["dict_test_f1"] for r in ue]), "holds": diff >= 0.15}
    if ex:
        pred["q_b"] = {"agent": out["explained"]["agent_f1_median"], "dict": out["explained"]["dict_f1_median"],
                       "holds": out["explained"]["agent_f1_median"] >= out["explained"]["dict_f1_median"] - 0.05}
    if rd and real:
        gap = med([r["test_f1"] for r in real]) - out["random"]["agent_f1_median"]
        pred["q_c"] = {"real_minus_random_f1": gap, "random_low_confidence_rate": out["random"]["low_confidence_rate"],
                       "holds": gap >= 0.2 and out["random"]["low_confidence_rate"] >= 0.5}
    if real:
        sh = med([r["sim_share"] for r in real])
        pred["q_d"] = {"real_sim_share_median": sh, "holds": sh is not None and sh >= 0.5}
    if rd and real and NC["study"] == "r":  # (r-f) each real unit against the random-direction null of the study
        p90 = float(np.percentile([r["test_f1"] for r in rd], 90))
        frac = float(np.mean([r["test_f1"] > p90 for r in real]))
        pred["r_f"] = {"random_f1_p90": p90, "real_frac_above_random_p90": frac, "holds": frac >= 0.5}
    out["predictions"] = pred
    return out


def write_md(rep):
    L = ["# Neuron Scientist: held-out verification", "", "Test split = validation games (never read by the describing agent).", ""]
    s = rep["summary"]
    L += ["| stratum | n | agent F1 (median) | dictionary F1 | AUROC | simulation share of ceiling | synthesis beats max | low confidence |",
          "|---|---|---|---|---|---|---|---|"]
    f = lambda x: "-" if x is None else f"{x:.2f}"
    for k in ("explained", "unexplained", "random"):
        v = s[k]
        L.append(f"| {k} | {v['n']} | {f(v['agent_f1_median'])} | {f(v['dict_f1_median'])} | {f(v['auroc_median'])} | {f(v['sim_share_median'])} | "
                 f"{f(v['synthesis_rate'])} | {f(v['low_confidence_rate'])} |")
    L += ["", f"Pre-registered predictions (PLAN.md addendum {'r' if NC['min_ply'] else 'q'}; q_x keys = the same tests):", ""]
    for k, v in s["predictions"].items():
        L.append(f"- {k}: {'HOLDS' if v['holds'] else 'FAILS'} - " + ", ".join(f"{a}={b}" for a, b in v.items() if a != "holds"))
    if rep.get("judge"):
        L.append(f"- q_e (text-only judge): {rep['judge']}")
    L += ["", "| unit | stratum | layer/neuron | pole | F1 | dict F1 (concept) | sim share | conf | description |", "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rep["rows"], key=lambda r: (r["stratum"], -r["test_f1"])):
        L.append(f"| {r['unit']} | {r['stratum']} | L{r['layer']}/{r['neuron'] if r['neuron'] is not None else 'rand'} | {r['pole']} | {r['test_f1']:.2f} | "
                 f"{r['dict_test_f1']:.2f} ({r['dict_concept']}) | {f(r['sim_share'])} | {r['confidence']} | {r['description'].replace('|', '/')} |")
    (ns.NS / "report.md").write_text("\n".join(L) + "\n")


def cmd_judge_export(a):
    desc = load_descriptions()
    key, st = ns.unit_key(), ns.stats()
    model = ns.load_web_model()
    us = sorted(desc)
    tmoves, _, tlen = ns.load_games(ns.TEST_SPLIT, NC["n_games"])
    S = test_acts(model, us, key)
    bs = ns.BoardSet(tmoves, tlen)
    out = ns.NS / "judge"; out.mkdir(exist_ok=True)
    answers = {}
    for j, u in enumerate(us):
        rng = np.random.default_rng(1000 + j)
        sign = st[u]["sign"]
        el = ns.eligible(tlen, NC["min_ply"])  # (r) judge pairs use eligible positions only
        fire = ns.fires_from(S[:, j], st, u) & el
        p90 = np.percentile(sign * S[el, j], 90)
        pos, neg = np.flatnonzero(fire), np.flatnonzero((sign * S[:, j] < p90) & el)
        n = min(NC["judge_pairs"], len(pos))
        pairs, key_ = [], []
        for pi, ni in zip(rng.choice(pos, n, replace=False), rng.choice(neg, n, replace=False)):
            first = rng.random() < 0.5
            A, B = (pi, ni) if first else (ni, pi)
            pairs.append({"A": {"moves": bs.board(int(A)).moves, "board": bs.board(int(A)).render()},
                          "B": {"moves": bs.board(int(B)).moves, "board": bs.board(int(B)).render()}})
            key_.append("A" if first else "B")
        (out / f"{u}.json").write_text(json.dumps({"unit": u, "description": desc[u]["description"], "pairs": pairs}, indent=1))
        answers[u] = key_
    (ns.PRIVATE / "judge_key.json").write_text(json.dumps(answers))
    print(f"wrote {len(us)} judge packs to ns/judge/")


def cmd_judge_score(a):
    key = json.loads((ns.PRIVATE / "judge_key.json").read_text())
    k = ns.unit_key()
    acc = {}
    for f in sorted((ns.NS / "judge_answers").glob("U*.json")):
        u = f.stem
        ans = json.loads(f.read_text())["answers"]
        acc[u] = float(np.mean([x == y for x, y in zip(ans, key[u])]))
    real = [v for u, v in acc.items() if k[u]["kind"] == "neuron"]
    rnd = [v for u, v in acc.items() if k[u]["kind"] != "neuron"]
    j = {"per_unit": acc, "real_mean": float(np.mean(real)) if real else None, "random_mean": float(np.mean(rnd)) if rnd else None}
    j["q_e_holds"] = j["real_mean"] is not None and j["real_mean"] >= 0.8
    rep = json.loads((ns.NS / "report.json").read_text())
    rep["judge"] = j
    (ns.NS / "report.json").write_text(json.dumps(rep, indent=1))
    write_md(rep)
    print(json.dumps({k_: v for k_, v in j.items() if k_ != "per_unit"}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("run"); sp.add_parser("judge-export"); sp.add_parser("judge-score")
    a = p.parse_args()
    torch.set_grad_enabled(False)
    {"run": cmd_run, "judge-export": cmd_judge_export, "judge-score": cmd_judge_score}[a.cmd](a)


if __name__ == "__main__":
    main()
