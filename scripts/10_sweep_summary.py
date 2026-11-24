"""Aggregate the width sweep and test the pre-registered predictions W1-W3 (docs/PLAN.md addendum c).

Reads results/sweep/w<d_ff>_s<seed>/{train_curve_*,play_*,sparsity,concepts_summary,modes}.json and writes
results/sweep_summary.json with per-run values, per-width seed means, and for each prediction whether the seed-mean
sequence over widths is monotone in the predicted direction (and its Spearman correlation with log width).
"""
import json

import numpy as np

from c4n import config, provenance

CFG = config.load()
WIDTHS = [256, 512, 1024, 2048, 4096]
SEEDS = [1, 2]


def load(run, name):
    p = config.ROOT / "results" / "sweep" / run / name
    return json.loads(p.read_text()) if p.exists() else None


def spearman(x, y):
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


def metrics(run):
    m = {}
    tc = load(run, f"train_curve_{run}.json")
    if tc:
        m["params"] = tc["params"]
        m["val_agree"] = tc["curve"][-1]["agree"]
        m["val_kl"] = tc["curve"][-1]["kl"]
    play = load(run, f"play_{run}_step_{CFG['train']['steps']:06d}.json")
    if play:
        m["win_vs_d10"] = play["results"]["teacher_d10"]["win"]
        m["score_vs_d10"] = play["results"]["teacher_d10"]["win"] + 0.5 * play["results"]["teacher_d10"]["draw"]
    sp = load(run, "sparsity.json")
    if sp:
        cond = {c["condition"]: c for c in sp["conditions"]}
        base = cond["intact"]["agree"]
        m["agree_intact"] = base
        for b in ("P25-P75", "P10-P90", "P5-P95"):
            m[f"cost_{b}"] = base - cond[f"band_{b}"]["agree"]
        m["keep_top64_agree"] = cond["keep_top64"]["agree"]
        m["keep_random64_agree"] = cond["keep_random64"]["agree"]
        m["firing_gate_pos"] = sp["quadrants"]["gate+ up+"]["firing"] + sp["quadrants"]["gate+ up-"]["firing"]
    cs = load(run, "concepts_summary.json")
    if cs:
        n, r = cs["neurons"]["f1_sweep"], cs["random_rotation"]["f1_sweep"]
        m["share_f1_ge_0.5_neurons"] = n["share_ge_0.5"]
        m["share_f1_ge_0.5_rotation"] = r["share_ge_0.5"]
        m["neuron_minus_rotation"] = n["share_ge_0.5"] - r["share_ge_0.5"]
        m["median_f1_p97_neurons"] = cs["neurons"]["f1_p97"]["median"]
        m["median_f1_p97_rotation"] = cs["random_rotation"]["f1_p97"]["median"]
    md = load(run, "modes.json")
    if md:
        s = md["summary_random_sample"]
        m["share_top_mode_ge_0.9"] = s["share_top_mode_ge_0.9"]
        m["modes_mean"] = s["modes_mean"]
    return m


def main():
    runs = {f"w{w}_s{s}": metrics(f"w{w}_s{s}") for w in WIDTHS for s in SEEDS}
    keys = sorted({k for m in runs.values() for k in m})
    by_width = {}
    for w in WIDTHS:
        by_width[w] = {}
        for k in keys:
            vals = [runs[f"w{w}_s{s}"][k] for s in SEEDS if k in runs[f"w{w}_s{s}"]]
            if vals:
                by_width[w][k] = {"mean": float(np.mean(vals)), "values": vals}
    tests = {}
    for name, key, direction in (("W1", "cost_P5-P95", "down"), ("W2", "neuron_minus_rotation", "up"),
                                 ("W3", "share_top_mode_ge_0.9", "up")):
        seq = [by_width[w][key]["mean"] for w in WIDTHS if key in by_width[w]]
        if len(seq) < len(WIDTHS):
            tests[name] = {"metric": key, "status": "incomplete", "n_widths": len(seq)}
            continue
        d = np.diff(seq)
        mono = bool(np.all(d < 0)) if direction == "down" else bool(np.all(d > 0))
        rho = spearman(np.log2(WIDTHS), seq)
        res = {"metric": key, "direction": direction, "seed_means": seq, "strictly_monotone": mono,
               "spearman_vs_log_width": rho}
        if name == "W2":
            res["positive_at_4096"] = seq[-1] > 0
            res["holds"] = mono and seq[-1] > 0
        else:
            res["holds"] = mono
        tests[name] = res
    out = config.ROOT / "results" / "sweep_summary.json"
    out.write_text(json.dumps({"widths": WIDTHS, "seeds": SEEDS, "runs": runs, "by_width": by_width, "predictions": tests}, indent=1))
    provenance.write(out, CFG)
    for k, v in tests.items():
        print(k, json.dumps(v))


if __name__ == "__main__":
    main()
