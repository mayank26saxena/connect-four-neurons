"""Concept coverage (PLAN.md addendum (o)): how many ground-truth concepts can be mapped to one unit, to one random direction,
or to one linear direction (probe) on the residual stream? Cross-fitted: the unit / direction / threshold is chosen on one half
of the games and scored by F1 on the other half (two folds). Writes <results_dir>/concept_coverage.json.
SMOKE=1: 300 games."""
import json
import os

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n import worldmodel as WM
from c4n.concepts import FAMILY, NAMES
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, XC = CFG["analysis"], CFG["crossfit"]
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PCTS = XC["pcts"]
PROBS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
N_BOOT = 500


def f1_mat(fire, C, cnt):
    tp = fire.T @ C
    return 2 * tp / (fire.sum(0)[:, None] + cnt[None, :]).clamp_min(1)


def f1_cols(fire, C):
    """F1 of fire[:, k] against C[:, k] for every concept k."""
    tp = (fire * C).sum(0)
    return 2 * tp / (fire.sum(0) + C.sum(0)).clamp_min(1)


@torch.no_grad()
def best_units(acts, CA, A_idx, rot):
    """For every concept: best (layer, neuron, side, pct) on the A half. Returns F1_A (K,), and per-concept spec arrays."""
    L, Fd = acts.shape[1], acts.shape[2]
    K = CA.shape[1]
    cnt = CA.sum(0)
    best = torch.full((K,), -1.0, device=DEV)
    spec = torch.zeros(K, 5, device=DEV)  # layer, neuron, side, threshold value, ... (4 used)
    for l in range(L):
        XA = acts[:, l].index_select(0, A_idx).to(DEV).float()
        Rl = rot[l].to(DEV) if rot is not None else None
        for c0 in range(0, Fd, XC["col_chunk"]):
            xa = XA[:, c0:c0 + XC["col_chunk"]] if Rl is None else XA @ Rl[:, c0:c0 + XC["col_chunk"]]
            s = xa.sort(0).values
            nA = xa.shape[0]
            for side in (0, 1):
                for p in PCTS:
                    q = p if side == 0 else 100 - p
                    t = s[min(nA - 1, int(round(q / 100 * (nA - 1))))]
                    fire = ((xa > t) if side == 0 else (xa < t)).float()
                    f, j = f1_mat(fire, CA, cnt).max(0)  # per concept: best unit in this chunk
                    upd = f > best
                    if upd.any():
                        best = torch.where(upd, f, best)
                        spec[upd, 0] = l; spec[upd, 1] = (c0 + j[upd]).float(); spec[upd, 2] = side
                        spec[upd, 3] = t[j[upd]]
    return best, spec


@torch.no_grad()
def fire_on_B(acts, spec, B_idx, rot):
    """(nB, K) float: the selected unit of each concept, fired on the B half."""
    K = spec.shape[0]
    nB = len(B_idx)
    out = torch.zeros(nB, K, device=DEV)
    for l in spec[:, 0].long().unique().tolist():
        ks = torch.nonzero(spec[:, 0] == l).squeeze(1)
        XB = acts[:, l].index_select(0, B_idx).to(DEV).float()
        if rot is not None:
            XB = XB @ rot[l].to(DEV)
        x = XB[:, spec[ks, 1].long()]
        t, side = spec[ks, 3][None], spec[ks, 2][None]
        out[:, ks] = torch.where(side == 0, x > t, x < t).float()
    return out


@torch.no_grad()
def probe_fire(X, CA, CB, A_idx, B_idx, points, steps):
    """Linear probe per concept at each read point; best point and probability threshold chosen on A. Returns (nB, K) fire on B and
    F1_A (K,)."""
    K = CA.shape[1]
    bestA = torch.full((K,), -1.0, device=DEV)
    fire_best = torch.zeros(len(B_idx), K, device=DEV)
    cnt = CA.sum(0)
    for pi in range(len(points)):
        Xa = X[A_idx, pi]
        with torch.enable_grad():
            W, b = WM.fit_binary(Xa, CA.cpu(), DEV, steps=steps, seed=CFG["seed"])
        sa = torch.sigmoid(Xa.to(DEV).float() @ W + b)
        sb = torch.sigmoid(X[B_idx, pi].to(DEV).float() @ W + b)
        for p in PROBS:
            f = f1_cols((sa > p).float(), CA)
            upd = f > bestA
            if upd.any():
                bestA = torch.where(upd, f, bestA)
                fire_best[:, upd] = (sb[:, upd] > p).float()
    return fire_best, bestA


def main():
    torch.manual_seed(CFG["seed"])
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    moves, _, lengths = load_split(CFG, "analysis")
    n = 300 if os.environ.get("SMOKE") else AC["n_games"]
    C = concepts_for(CFG, "analysis", AC["n_games"])[: int(lengths[:n].sum())]
    acts, _, _ = A.collect(model, moves[:n], lengths[:n], DEV)
    X = WM.collect_points(model, moves[:n], lengths[:n], DEV, WM.block_points(L))
    gid, _ = A.valid_index(lengths[:n])
    cc = C.sum(0)
    usable = (cc >= XC["min_concept_count"]) & (cc <= C.shape[0] - XC["min_concept_count"])
    Cu = torch.as_tensor(C[:, usable], dtype=torch.float32)
    names = [NAMES[k] for k in np.flatnonzero(usable)]
    fam = np.array([FAMILY[k] for k in np.flatnonzero(usable)])
    K = Cu.shape[1]
    rot = A.random_rotations(L, Fd, AC["rotation_seed"], DEV)
    half = n // 2
    folds = [(np.flatnonzero(gid < half), np.flatnonzero(gid >= half)), (np.flatnonzero(gid >= half), np.flatnonzero(gid < half))]
    methods = ("neuron", "rotation", "probe")
    held = {m: [] for m in methods}      # per fold: held-out F1 (K,)
    boots = {m: [] for m in methods}     # per fold: (R,) coverage share per bootstrap resample
    for fi, (a_i, b_i) in enumerate(folds):
        A_idx, B_idx = torch.as_tensor(a_i), torch.as_tensor(b_i)
        CA, CB = Cu[A_idx].to(DEV), Cu[B_idx].to(DEV)
        gB = np.unique(gid[b_i], return_inverse=True)[1]
        G = int(gB.max()) + 1
        W = torch.as_tensor(rng.multinomial(G, [1 / G] * G, size=N_BOOT).T, dtype=torch.float32, device=DEV)
        gBt = torch.as_tensor(gB, device=DEV)
        for m in methods:
            if m == "probe":
                fire, _ = probe_fire(X, CA, CB, A_idx, B_idx, WM.block_points(L), XC.get("probe_steps", 300))
            else:
                _, spec = best_units(acts, CA, A_idx, rot if m == "rotation" else None)
                fire = fire_on_B(acts, spec, B_idx, rot if m == "rotation" else None)
            f1 = f1_cols(fire, CB)
            held[m].append(f1.cpu().numpy())
            both = fire * CB
            tpg = torch.zeros(G, K, device=DEV).index_add_(0, gBt, both)
            fcg = torch.zeros(G, K, device=DEV).index_add_(0, gBt, fire)
            pog = torch.zeros(G, K, device=DEV).index_add_(0, gBt, CB)
            F = 2 * (W.T @ tpg) / (W.T @ fcg + W.T @ pog).clamp_min(1)  # (R, K)
            boots[m].append((F >= 0.5).float().mean(1).cpu().numpy())
            print(f"fold {fi} {m}: coverage {(f1 >= 0.5).float().mean().item():.3f} mean F1 {f1.mean().item():.3f}", flush=True)
    out = {"model": model.cfg, "checkpoint": AC["checkpoint"], "n_games": n, "n_concepts": int(K), "n_units": int(L * Fd * 2), "coverage": {}, "by_family": {}}
    cov = {m: np.mean([(h >= 0.5) for h in held[m]], 0) for m in methods}     # (K,) share over folds
    mean_f1 = {m: np.mean(held[m], 0) for m in methods}
    bt = {m: np.mean(boots[m], 0) for m in methods}
    ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    for m in methods:
        out["coverage"][m] = {"share": float(cov[m].mean()), "ci95": ci(bt[m]), "mean_f1": float(mean_f1[m].mean())}
    out["diff"] = {"neuron_minus_rotation": {"mean": float(cov["neuron"].mean() - cov["rotation"].mean()), "ci95": ci(bt["neuron"] - bt["rotation"])},
                   "probe_minus_neuron": {"mean": float(cov["probe"].mean() - cov["neuron"].mean()), "ci95": ci(bt["probe"] - bt["neuron"])}}
    for f in sorted(set(fam)):
        s = fam == f
        out["by_family"][f] = {"n": int(s.sum()), **{m: float(cov[m][s].mean()) for m in methods}}
    out["concepts"] = [{"name": nm, "family": fm, **{m: float(mean_f1[m][i]) for m in methods}} for i, (nm, fm) in enumerate(zip(names, fam))]
    path = config.results_dir(CFG) / ("concept_coverage_smoke.json" if os.environ.get("SMOKE") else "concept_coverage.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, CFG)
    print(json.dumps({"coverage": out["coverage"], "diff": out["diff"]}))


if __name__ == "__main__":
    main()
