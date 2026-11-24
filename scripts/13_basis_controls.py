"""T1 / T2: is the neuron basis special in itself, independent of any concept vocabulary?

T1  Shape: mean excess kurtosis of each unit's activation distribution, and the share of squared activation held by the
    largest 5% of entries, in the neuron basis vs random orthogonal rotations of each layer's hidden space.
T2  Function: agreement with the intact model's policy (and KL) after zeroing each unit's central band, or keeping only the
    largest `topk_frac` of units per position, in the neuron basis vs the rotated basis. Rotated-basis interventions rotate
    the hidden activation, edit it, and rotate back (the rotation is orthogonal, so with nothing zeroed it is the identity).
Writes basis_controls.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.data import flat_scores, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, BC = CFG["analysis"], CFG["basis"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def shape_stats(X, sub, seed):
    """X (N, F) float. Mean/median excess kurtosis over units; share of squared activation in the top 5% of entries."""
    xc = X - X.mean(0, keepdim=True)
    v = xc.pow(2).mean(0).clamp_min(1e-12)
    kurt = xc.pow(4).mean(0) / v.pow(2) - 3.0
    g = torch.Generator().manual_seed(seed)
    idx = torch.randint(0, X.numel(), (sub,), generator=g).to(X.device)
    e = X.reshape(-1)[idx].pow(2).sort(descending=True).values
    return kurt.mean().item(), kurt.median().item(), (e[: int(0.05 * sub)].sum() / e.sum()).item()


def rot_band_hook(Rs, lo, hi):
    def hook(l, a, g, u):
        r = a @ Rs[l]
        return ((r * ((r <= lo[l]) | (r >= hi[l]))) @ Rs[l].T)
    return hook


def rot_topk_hook(Rs, k):
    def hook(l, a, g, u):
        r = a @ Rs[l]
        m = torch.zeros_like(r).scatter_(-1, r.abs().topk(k, -1).indices, 1.0)
        return (r * m) @ Rs[l].T
    return hook


def main():
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, lengths = moves[:n], lengths[:n]
    fs = flat_scores(scores[:n], lengths)
    acts, _, ref = A.collect(model, moves, lengths, DEV)
    L, Fd = acts.shape[1], acts.shape[2]
    pairs = BC["bands"]
    qs = sorted({q for lo, hi in pairs for q in (lo, hi)})
    k = int(BC["topk_frac"] * Fd)
    seeds = [AC["rotation_seed"] + s for s in range(BC["rotation_seeds"])]
    out = {"n_positions": int(acts.shape[0]), "d_ff": Fd, "topk": k, "rotation_seeds": seeds}

    # ---- T1: shape ----
    kn = [shape_stats(acts[:, l].to(DEV).float(), BC["kurt_subsample"], l) for l in range(L)]
    kr = []
    rots = []
    for s in seeds:
        R = A.random_rotations(L, Fd, s, DEV)
        rots.append(R)
        kr.append([shape_stats(acts[:, l].to(DEV).float() @ R[l].to(DEV), BC["kurt_subsample"], l) for l in range(L)])
    out["kurtosis_mean"] = {"neuron": float(np.mean([a[0] for a in kn])), "rotation": float(np.mean([[a[0] for a in r] for r in kr]))}
    out["kurtosis_median"] = {"neuron": float(np.mean([a[1] for a in kn])), "rotation": float(np.mean([[a[1] for a in r] for r in kr]))}
    out["top5_energy"] = {"neuron": float(np.mean([a[2] for a in kn])), "rotation": float(np.mean([[a[2] for a in r] for r in kr]))}
    out["kurtosis_by_layer"] = {"neuron": [a[0] for a in kn], "rotation": [float(np.mean([r[l][0] for r in kr])) for l in range(L)]}
    print("T1", json.dumps({k_: out[k_] for k_ in ("kurtosis_mean", "kurtosis_median", "top5_energy")}), flush=True)

    # ---- T2: function ----
    def metrics(hook):
        lg = A.collect_logits(model, moves, lengths, DEV, batch=BC["batch"], hook=hook)
        return A.policy_metrics(lg, ref, fs)

    base = A.policy_metrics(ref, ref, fs)
    P = A.percentiles(acts, qs, DEV)  # neuron basis percentiles (len(qs), L, F)
    pi = {q: i for i, q in enumerate(qs)}
    cond = {"intact": {"agree": base["agree"]}}
    for lo, hi in pairs:
        name = f"band_P{lo}-P{hi}"
        nb = metrics(A.band_ablation_hook(P[pi[lo]].to(DEV), P[pi[hi]].to(DEV)))
        rb = []
        for R in rots:
            Rs = [R[l].to(DEV) for l in range(L)]
            lo_r, hi_r = torch.empty(L, Fd), torch.empty(L, Fd)
            for l in range(L):
                Q = A.percentiles((acts[:, l].to(DEV).float() @ Rs[l]).half().unsqueeze(1), [lo, hi], DEV)
                lo_r[l], hi_r[l] = Q[0, 0], Q[1, 0]
            rb.append(metrics(rot_band_hook(Rs, lo_r.to(DEV), hi_r.to(DEV))))
        cond[name] = {"neuron": nb, "rotation": rb}
        print(name, "neuron", round(nb["agree"], 3), "rotation", [round(r["agree"], 3) for r in rb], flush=True)
    nt = metrics(A.topk_hook(k, "top"))
    rt = [metrics(rot_topk_hook([R[l].to(DEV) for l in range(L)], k)) for R in rots]
    cond[f"keep_top{k}"] = {"neuron": nt, "rotation": rt}
    print("topk", round(nt["agree"], 3), [round(r["agree"], 3) for r in rt], flush=True)
    out["conditions"] = cond
    path = config.results_dir(CFG) / "basis_controls.json"
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
