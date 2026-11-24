"""T3: cross-fitted concept matching with game-level bootstrap intervals, neurons vs random rotations.

For each fold (games split in half, then the reverse): every pole picks its best (concept, firing threshold) on the
training half, where the threshold is an absolute activation value taken from a tail percentile of that half. The pole is
then scored by F1 on the held-out half with that same concept and threshold, so selection bias does not inflate the score.
Game-level bootstrap (resampling held-out games with multinomial weights, shared by both bases) gives paired 95% intervals
for the share of poles with held-out F1 >= 0.5 and for the neuron-minus-rotation difference. Writes crossfit.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import FAMILY
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, XC = CFG["analysis"], CFG["crossfit"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
PCTS = XC["pcts"]


def f1_mat(fire, C, cnt):
    tp = fire.T @ C
    return 2 * tp / (fire.sum(0)[:, None] + cnt[None, :]).clamp_min(1)


@torch.no_grad()
def run_fold(acts, Cu, gid, A_idx, B_idx, rotation, W, fam_of_k):
    """Returns dict(insample_hits, heldout_hits, boot_hits (R,), n, families {fam: held>=0.5 count})."""
    L, Fd = acts.shape[1], acts.shape[2]
    CA, CB = Cu[A_idx].to(DEV), Cu[B_idx].to(DEV)
    cntA = CA.sum(0)
    gB = torch.as_tensor(gid[B_idx.numpy()], device=DEV)
    R_ = W.shape[1]
    res = {"in": 0, "held": 0, "n": 0, "boot": torch.zeros(R_, device=DEV), "fam": {}}
    for l in range(L):
        XA = acts[:, l].index_select(0, A_idx).to(DEV).float()
        XB = acts[:, l].index_select(0, B_idx).to(DEV).float()
        Rl = rotation[l].to(DEV) if rotation is not None else None
        for c0 in range(0, Fd, XC["col_chunk"]):
            xa = XA[:, c0:c0 + XC["col_chunk"]] if Rl is None else XA @ Rl[:, c0:c0 + XC["col_chunk"]]
            xb = XB[:, c0:c0 + XC["col_chunk"]] if Rl is None else XB @ Rl[:, c0:c0 + XC["col_chunk"]]
            c = xa.shape[1]
            s = xa.sort(0).values
            nA = xa.shape[0]
            for side in (0, 1):
                thr = []
                best = torch.full((c,), -1.0, device=DEV)
                bp = torch.zeros(c, dtype=torch.long, device=DEV)
                bk = torch.zeros(c, dtype=torch.long, device=DEV)
                for pi, p in enumerate(PCTS):
                    q = p if side == 0 else 100 - p
                    t = s[min(nA - 1, int(round(q / 100 * (nA - 1))))]
                    thr.append(t)
                    fire = ((xa > t) if side == 0 else (xa < t)).float()
                    b, k = f1_mat(fire, CA, cntA).max(1)
                    upd = b > best
                    best = torch.where(upd, b, best); bp = torch.where(upd, torch.full_like(bp, pi), bp); bk = torch.where(upd, k, bk)
                tsel = torch.stack(thr)[bp, torch.arange(c, device=DEV)]
                fireB = ((xb > tsel) if side == 0 else (xb < tsel)).float()
                Cb = CB[:, bk]
                both = fireB * Cb
                tp, fc, pos = both.sum(0), fireB.sum(0), Cb.sum(0)
                held = 2 * tp / (fc + pos).clamp_min(1)
                res["in"] += (best >= 0.5).sum().item(); res["held"] += (held >= 0.5).sum().item(); res["n"] += c
                tpg = torch.zeros(int(gB.max()) + 1, c, device=DEV).index_add_(0, gB, both)
                fcg = torch.zeros_like(tpg).index_add_(0, gB, fireB)
                pog = torch.zeros_like(tpg).index_add_(0, gB, Cb)
                tpR, fcR, poR = tpg.T @ W, fcg.T @ W, pog.T @ W
                res["boot"] += ((2 * tpR / (fcR + poR).clamp_min(1)) >= 0.5).sum(0).float()
                for j in torch.nonzero(held >= 0.5).squeeze(1).tolist():
                    f = fam_of_k[bk[j].item()]
                    res["fam"][f] = res["fam"].get(f, 0) + 1
    res["boot"] = res["boot"].cpu().numpy()
    return res


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, _, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    C = concepts_for(CFG, "analysis", n)
    acts, _, _ = A.collect(model, moves[:n], lengths[:n], DEV)
    L, Fd = acts.shape[1], acts.shape[2]
    gid, _ = A.valid_index(lengths[:n])
    cc = C.sum(0)
    usable = (cc >= XC["min_concept_count"]) & (cc <= C.shape[0] - XC["min_concept_count"])
    Cu = torch.as_tensor(C[:, usable], dtype=torch.float32)
    fam_of_k = [FAMILY[k] for k in np.flatnonzero(usable)]
    rot = A.random_rotations(L, Fd, AC["rotation_seed"], DEV)
    half = n // 2
    folds = [(np.flatnonzero(gid < half), np.flatnonzero(gid >= half)), (np.flatnonzero(gid >= half), np.flatnonzero(gid < half))]
    out = {"n_games": n, "n_boot": XC["n_boot"], "folds": 2}
    agg = {"neuron": [], "rotation": []}
    for fi, (a_i, b_i) in enumerate(folds):
        A_idx, B_idx = torch.as_tensor(a_i), torch.as_tensor(b_i)
        gB = np.unique(gid[b_i], return_inverse=True)[1]
        G = int(gB.max()) + 1
        W = torch.as_tensor(rng.multinomial(G, [1 / G] * G, size=XC["n_boot"]).T, dtype=torch.float32, device=DEV)
        for name, R in (("neuron", None), ("rotation", rot)):
            gid_local = np.zeros_like(gid); gid_local[b_i] = gB
            agg[name].append(run_fold(acts, Cu, gid_local, A_idx, B_idx, R, W, fam_of_k))
            r = agg[name][-1]
            print(f"fold {fi} {name}: in-sample {r['in'] / r['n']:.4f} held-out {r['held'] / r['n']:.4f}", flush=True)
    for name in agg:
        n_p = sum(r["n"] for r in agg[name])
        out[name] = {"n_poles": n_p, "share_insample": sum(r["in"] for r in agg[name]) / n_p, "share_heldout": sum(r["held"] for r in agg[name]) / n_p,
                     "families_heldout": {f: sum(r["fam"].get(f, 0) for r in agg[name]) // 2 for f in sorted({f for r in agg[name] for f in r["fam"]})}}
        boot = np.mean([r["boot"] / r["n"] for r in agg[name]], axis=0)
        out[name]["share_heldout_ci95"] = [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
    dboot = np.mean([agg["neuron"][i]["boot"] / agg["neuron"][i]["n"] - agg["rotation"][i]["boot"] / agg["rotation"][i]["n"] for i in range(2)], axis=0)
    out["diff_heldout"] = {"mean": out["neuron"]["share_heldout"] - out["rotation"]["share_heldout"],
                           "ci95": [float(np.percentile(dboot, 2.5)), float(np.percentile(dboot, 97.5))]}
    out["diff_insample"] = out["neuron"]["share_insample"] - out["rotation"]["share_insample"]
    path = config.results_dir(CFG) / "crossfit.json"
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, CFG)
    print(json.dumps({"neuron": out["neuron"]["share_heldout"], "rotation": out["rotation"]["share_heldout"], "diff": out["diff_heldout"]}))


if __name__ == "__main__":
    main()
