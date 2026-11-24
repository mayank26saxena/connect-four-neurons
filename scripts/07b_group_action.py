"""Q5b: redundancy. Do groups of concept-matched neurons carry the behaviour that single neurons do not?

For each action concept (block_now_c{c}, win_now_c{c}; c = 0..6):
1. Rank every pole by F1 between its firing (beyond p97 / p3) and that exact concept.
2. Necessity: zero the neurons of the top-k poles (k in `group.ks`) at every position, and measure the rate of playing
   column c on positions where the concept holds. Baseline: k random neurons drawn with the same per-layer counts
   (`group.n_random` draws).
3. Sufficiency: clamp the top-k poles to their p99.5 / p0.5 value at the evaluated position, on positions where the
   concept does not hold and column c is legal, and measure the rate of playing c.
Writes group_action.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import INDEX
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint, tokens_from_moves

CFG = config.load()
AC, GC = CFG["analysis"], CFG["group"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
FIRE = AC["fire_pct"]


@torch.no_grad()
def concept_f1_all_poles(acts, c, hi, lo):
    """F1 of every pole against one concept vector c (N,) bool. Returns (L, F, 2)."""
    N, L, Fd = acts.shape
    cv = torch.as_tensor(c, device=DEV, dtype=torch.float32)
    out = torch.zeros((L, Fd, 2))
    for l in range(L):
        for c0 in range(0, Fd, 512):  # neuron blocks bound GPU memory for wide layers
            X = acts[:, l, c0:c0 + 512].to(DEV).float()
            for s, fire in ((0, X > hi[l, c0:c0 + 512].to(DEV)), (1, X < lo[l, c0:c0 + 512].to(DEV))):
                f = fire.float()
                tp = f.T @ cv
                out[l, c0:c0 + 512, s] = (2 * tp / (f.sum(0) + cv.sum()).clamp_min(1)).cpu()
    return out


def make_hook(neurons_by_layer, values_by_layer=None, tt=None):
    idx = {l: torch.as_tensor(n, device=DEV) for l, n in neurons_by_layer.items() if len(n)}
    vals = {l: torch.as_tensor(v, device=DEV, dtype=torch.float32) for l, v in (values_by_layer or {}).items() if len(v)}

    def hook(l, a, g, u):
        if l not in idx:
            return a
        a = a.clone()
        if values_by_layer is None:
            a[..., idx[l]] = 0.0
        else:
            rows = torch.arange(a.shape[0], device=DEV)
            a[rows[:, None], tt[:, None], idx[l][None, :]] = vals[l][None, :]
        return a
    return hook


@torch.no_grad()
def play_rate(model, moves, legal_all, games, ts, col, build_hook=None, bs=1024):
    hits = 0
    for i in range(0, len(games), bs):
        g, t = games[i:i + bs], ts[i:i + bs]
        tok = tokens_from_moves(torch.as_tensor(moves[g])).to(DEV)
        tt = torch.as_tensor(t, device=DEV)
        lg = model(tok, hook=None if build_hook is None else build_hook(tt))
        lg = lg[torch.arange(len(g), device=DEV), tt]
        legal = torch.as_tensor(legal_all[g, t], device=DEV)
        hits += (lg.masked_fill(~legal, -1e9).argmax(-1) == col).sum().item()
    return hits / max(1, len(games))


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, lengths = moves[:n], lengths[:n]
    C = concepts_for(CFG, "analysis", n)
    gidx, tidx = A.valid_index(lengths)
    oh = np.zeros(moves.shape + (7,), dtype=np.int16)
    gg, tt_ = np.nonzero(moves >= 0)
    oh[gg, tt_, moves[gg, tt_]] = 1
    legal_all = (np.cumsum(oh, 1) - oh) < 6
    acts, _, _ = A.collect(model, moves, lengths, DEV)
    L, Fd = acts.shape[1], acts.shape[2]
    hi, lo = A.percentiles(acts, [FIRE, 100 - FIRE], DEV)
    chi, clo = A.percentiles(acts, [GC["clamp_pct"], 100 - GC["clamp_pct"]], DEV)
    out = []
    for fam in GC["concepts"]:
        for col in range(7):
            name = f"{fam}_c{col}"
            k_idx = INDEX[name]
            f1 = concept_f1_all_poles(acts, C[:, k_idx], hi, lo)
            order = np.argsort(-f1.reshape(-1).numpy())  # flat index = (l * Fd + f) * 2 + side
            pos_t = np.flatnonzero(C[:, k_idx])
            pos_f = np.flatnonzero(~C[:, k_idx] & legal_all[gidx, tidx, col])
            pos_t = rng.choice(pos_t, min(len(pos_t), GC["max_positions"]), replace=False)
            pos_f = rng.choice(pos_f, min(len(pos_f), GC["max_positions"]), replace=False)
            rec = {"concept": name, "n_true": int(len(pos_t)), "n_false": int(len(pos_f)),
                   "top_f1": [round(float(f1.reshape(-1)[i]), 4) for i in order[:max(GC["ks"])]],
                   "top_poles": [[int(i // 2 // Fd), int(i // 2 % Fd), "+-"[int(i % 2)]] for i in order[:max(GC["ks"])]],
                   "true_intact": play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col),
                   "false_intact": play_rate(model, moves, legal_all, gidx[pos_f], tidx[pos_f], col), "by_k": []}
            for k in GC["ks"]:
                sel = order[:k]
                layers, neurons, sides = sel // 2 // Fd, sel // 2 % Fd, sel % 2
                by_layer = {l: sorted(set(neurons[layers == l].tolist())) for l in range(L)}
                abl = play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col, lambda tt, b=by_layer: make_hook(b))
                rnd = []
                for _ in range(GC["n_random"]):
                    rb = {l: rng.choice(Fd, len(v), replace=False).tolist() for l, v in by_layer.items()}
                    rnd.append(play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col, lambda tt, b=rb: make_hook(b)))
                vals = {l: [] for l in range(L)}
                nb = {l: [] for l in range(L)}
                for l, f, s in zip(layers, neurons, sides):
                    if f in nb[l]:
                        continue
                    nb[l].append(int(f)); vals[l].append(float(chi[l, f] if s == 0 else clo[l, f]))
                clamp = play_rate(model, moves, legal_all, gidx[pos_f], tidx[pos_f], col,
                                  lambda tt, b=nb, v=vals: make_hook(b, v, tt))
                rec["by_k"].append({"k": k, "true_ablated": abl, "true_random_mean": float(np.mean(rnd)),
                                    "true_random_min": float(np.min(rnd)), "false_clamped": clamp})
            out.append(rec)
            print(name, round(rec["true_intact"], 3), [(r["k"], round(r["true_ablated"], 3), round(r["true_random_mean"], 3), round(r["false_clamped"], 3)) for r in rec["by_k"]], flush=True)
    path = config.results_dir(CFG) / "group_action.json"
    path.write_text(json.dumps({"concepts": out}, indent=1))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
