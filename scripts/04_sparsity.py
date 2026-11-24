"""Q1 functional sparsity: zero weak activations and measure what the model loses.

Conditions: zero each per-neuron percentile band (lo, hi); keep the top-k / random-k neurons per position and layer,
or drop the top-k. Metrics: KL(intact || ablated) over legal moves, agreement with the teacher's best move, fraction
of activations zeroed, and play results. Writes results/sparsity.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.data import flat_scores, load_split
from c4n.model import load_checkpoint
from c4n.play import match

CFG = config.load()
AC = CFG["analysis"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def run_condition(model, moves, lengths, scores, ref, hook, name, frac):
    lg = A.collect_logits(model, moves, lengths, DEV, hook=hook)
    m = A.policy_metrics(lg, ref, scores)
    m.update(condition=name, frac_zeroed=frac)
    for opp in AC["play_opponents"]:
        r = match(model, DEV, tuple(opp), hook)
        m[f"play_{opp[0]}{'' if opp[0] == 'random' else '_d' + str(opp[1])}"] = r
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items() if not k.startswith("play")}),
          {k: round(v["win"], 2) for k, v in m.items() if k.startswith("play")}, flush=True)
    return m


def main():
    torch.manual_seed(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    fs = flat_scores(scores, lengths)
    acts, quad, ref = A.collect(model, moves, lengths, DEV, want_quad=True)
    pcts = sorted({p for b in AC["bands"] for p in b})
    P = A.percentiles(acts, pcts, DEV)
    pi = {p: i for i, p in enumerate(pcts)}
    rows = [run_condition(model, moves, lengths, fs, ref, None, "intact", 0.0)]
    for lo, hi in AC["bands"]:
        lo_t, hi_t = P[pi[lo]].to(DEV), P[pi[hi]].to(DEV)
        frac = float(np.mean([((acts[:, l].float() > P[pi[lo]][l]) & (acts[:, l].float() < P[pi[hi]][l])).float().mean().item()
                              for l in range(acts.shape[1])]))
        rows.append(run_condition(model, moves, lengths, fs, ref, A.band_ablation_hook(lo_t, hi_t), f"band_P{lo}-P{hi}", frac))
    d_ff = CFG["model"]["d_ff"]
    for k in AC["topk"]:
        rows.append(run_condition(model, moves, lengths, fs, ref, A.topk_hook(k, "top"), f"keep_top{k}", 1 - k / d_ff))
        rows.append(run_condition(model, moves, lengths, fs, ref, A.topk_hook(k, "random", CFG["seed"]), f"keep_random{k}", 1 - k / d_ff))
        rows.append(run_condition(model, moves, lengths, fs, ref, A.topk_hook(k, "bottom"), f"drop_top{k}", k / d_ff))
    # quadrant shares: all activations vs pole firings (beyond p97/p3)
    hi, lo = A.percentiles(acts, [AC["fire_pct"], 100 - AC["fire_pct"]], DEV)
    q_all = torch.zeros(4); q_fire = torch.zeros(4)
    for l in range(acts.shape[1]):  # per layer, to bound memory for wide models
        a = acts[:, l].float()
        fire = (a > hi[l]) | (a < lo[l])
        q_all += torch.bincount(quad[:, l].flatten().long(), minlength=4).float()
        q_fire += torch.bincount(quad[:, l][fire].long(), minlength=4).float()
    names = {3: "gate+ up+", 2: "gate+ up-", 0: "gate- up-", 1: "gate- up+"}
    quads = {names[q]: {"all": (q_all[q] / q_all.sum()).item(), "firing": (q_fire[q] / q_fire.sum()).item()} for q in names}
    out = config.results_dir(CFG) / "sparsity.json"
    out.write_text(json.dumps({"n_games": n, "n_positions": int(lengths.sum()), "conditions": rows, "quadrants": quads}, indent=1))
    provenance.write(out, CFG)
    print(json.dumps(quads, indent=1))


if __name__ == "__main__":
    main()
