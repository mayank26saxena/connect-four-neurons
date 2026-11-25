"""Output-side neuron tools (PLAN.md addendum (v), after Shone & Dunlap 2026).

A pole = (layer, neuron, sign s). Its output vector is s * w, w = the neuron's column of the down projection. A pole is active
where s * a > 0 with the gate open (gate pre-activation > 0); it fires where it is active and s * a is beyond its dev p97.
Pole ids: pid = (layer * d_ff + neuron) * 2 + (0 for +, 1 for -).

Read points follow `worldmodel.run`: point 0 = embeddings, 2l+1 = after attention l, 2l+2 = after MLP l ("after layer l").
Lenses are averages over positions of same-position Jacobians (a perturbation at position t, read at position t).
"""
from __future__ import annotations

import numpy as np
import torch

from . import worldmodel as WM
from .model import tokens_from_moves
from .tactics import position_index


def pid(l, n, s, Fd):
    return (l * Fd + n) * 2 + (0 if s > 0 else 1)


def unpid(p, Fd):
    return (p // 2) // Fd, (p // 2) % Fd, (1 if p % 2 == 0 else -1)


def centered(lg):
    return lg - lg.mean(-1, keepdim=True)


# ---------------------------------------------------------------- collection

@torch.no_grad()
def collect(model, moves, lengths, device, bs=256, points=(2, 4, 6, 8, 10, 12)):
    """Every valid position (game-major): activations a (N, L, F) float16, gate open (N, L, F) bool, centered logits (N, 7),
    residual stream at `points` (N, P, d) float16. All on the CPU."""
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    N = int(lengths.sum())
    A = torch.empty((N, L, Fd), dtype=torch.float16)
    G = torch.empty((N, L, Fd), dtype=torch.bool)
    R = torch.empty((N, len(points), model.cfg["d_model"]), dtype=torch.float16)
    LG = torch.empty((N, 7))
    ptr = 0
    for i in range(0, len(lengths), bs):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + bs])).to(device)
        ln = torch.as_tensor(lengths[i:i + bs], device=device)
        valid = torch.arange(42, device=device)[None] < ln[:, None]
        store = {}

        def mh(l, a, g, u):
            store[l] = (a[:, :42][valid], (g[:, :42] > 0)[valid]); return a
        lg, kept = WM.run(model, tok, mlp_hook=mh, keep=set(points))
        n = int(valid.sum())
        for l in range(L):
            A[ptr:ptr + n, l] = store[l][0].half().cpu(); G[ptr:ptr + n, l] = store[l][1].cpu()
        for j, p in enumerate(points):
            R[ptr:ptr + n, j] = kept[p][:, :42][valid].half().cpu()
        LG[ptr:ptr + n] = centered(lg[:, :42][valid].float()).cpu()
        ptr += n
    return {"a": A, "gate": G, "resid": R, "points": list(points), "logits": LG}


def thresholds(A, elig, device, q=97):
    """Per neuron: positive threshold p97 of a, negative threshold p3 of a, over eligible positions. (L, F) each."""
    from .analysis import percentiles
    P = percentiles(A[torch.as_tensor(elig)], [100 - q, q], device)
    return P[1], P[0]


def firing(a, gate, thr_pos, thr_neg, l):
    """Bool (N, F, 2): pole + / pole - fires, for layer l."""
    a, g = a[:, l].float(), gate[:, l]
    return torch.stack([(a > thr_pos[l].clamp_min(0)) & g, (a < thr_neg[l].clamp_max(0)) & g], -1)


# ---------------------------------------------------------------- lenses

def _rows(moves, lengths, sel, device):
    g, t = position_index(lengths)
    gg, tt = g[sel], t[sel]
    tok = tokens_from_moves(torch.as_tensor(moves[gg])).to(device)
    return tok, torch.as_tensor(tt, device=device)


def jacobians(model, moves, lengths, sel, device, bs=1000):
    """Mean same-position Jacobians over positions `sel` (flat indices):
    J[l] (7, d) = d centered logits / d residual after layer l, for l = 0..L-1;
    Rres[l] (d, d) = d residual after the last layer / d residual after layer l."""
    L, d = model.cfg["n_layer"], model.cfg["d_model"]
    J = torch.zeros(L, 7, d, device=device)
    Rres = torch.zeros(L, d, d, device=device)
    last = 2 * L
    n = 0
    for s in range(0, len(sel), bs):
        tok, tt = _rows(moves, lengths, sel[s:s + bs], device)
        B = tok.shape[0]
        ar = torch.arange(B, device=device)
        for l in range(L):
            pt = 2 * l + 2
            delta = torch.zeros(B, d, device=device, requires_grad=True)

            def rh(p, x, pt=pt):
                if p == pt:
                    x = x.clone(); x[ar, tt] = x[ar, tt] + delta
                return x
            with torch.enable_grad():
                lg, kept = WM.run(model, tok, resid_hook=rh, keep={last})
                out = centered(lg[ar, tt])
                xf = kept[last][ar, tt]
                for k in range(7):
                    J[l, k] += torch.autograd.grad(out[:, k].sum(), delta, retain_graph=True)[0].sum(0)
                if l == L - 1:
                    Rres[l] += torch.eye(d, device=device) * B
                else:
                    for k in range(d):
                        Rres[l, k] += torch.autograd.grad(xf[:, k].sum(), delta, retain_graph=k < d - 1)[0].sum(0)
        n += B
    return (J / n).cpu(), (Rres / n).cpu()


def out_vectors(model):
    """(L, F, d) output vectors w (columns of each layer's down projection)."""
    return torch.stack([b.mlp.down.weight.detach().T.float().cpu() for b in model.blocks])


# ---------------------------------------------------------------- probes

def fit_probes(X, Y, device, steps=500, lr=1e-2, wd=1e-4, seed=0):
    """Logistic probes for every column of Y (bool) on X (float): returns W_eff (d, K), b_eff (K) acting on raw X."""
    torch.manual_seed(seed)
    X = torch.as_tensor(X, device=device).float()
    Y = torch.as_tensor(Y, device=device).float()
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    W = torch.zeros(X.shape[1], Y.shape[1], device=device, requires_grad=True)
    b = torch.zeros(Y.shape[1], device=device, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=lr, weight_decay=0)
    for _ in range(steps):
        opt.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy_with_logits(Z @ W + b, Y) + wd * (W ** 2).sum()
        loss.backward(); opt.step()
    W_eff = (W / sd[:, None]).detach()
    b_eff = (b - (mu / sd) @ W).detach()
    return W_eff.cpu(), b_eff.cpu()


def auroc_cols(S, Y, device):
    """AUROC per column of scores S (N, K) against bool labels Y (N, K); NaN where a column is constant."""
    S = torch.as_tensor(S, device=device).float(); Y = torch.as_tensor(Y, device=device).bool()
    out = torch.full((S.shape[1],), float("nan"))
    for k in range(S.shape[1]):
        y = Y[:, k]; npos = int(y.sum()); nneg = len(y) - npos
        if npos == 0 or nneg == 0:
            continue
        r = torch.empty_like(S[:, k]); r[S[:, k].argsort()] = torch.arange(1, len(y) + 1, device=device, dtype=r.dtype)
        out[k] = float((r[y].sum() - npos * (npos + 1) / 2) / (npos * nneg))
    return out


def phi(Y, device):
    """Pearson correlation between bool columns (K, K); NaN rows for constant columns."""
    Yf = torch.as_tensor(Y, device=device).float()
    Yf = Yf - Yf.mean(0)
    sd = Yf.pow(2).mean(0).sqrt()
    C = (Yf.T @ Yf) / len(Yf)
    return (C / (sd[:, None] * sd[None, :])).cpu()


# ---------------------------------------------------------------- interventions

class PoleZero:
    """mlp hook that zeroes, row by row, one pole (layer l_r, neuron n_r, sign s_r) wherever it is active, at every position."""

    def __init__(self, l, n, s):
        self.l, self.n, self.s = l, n, s

    def __call__(self, layer, a, g, u):
        sel = torch.nonzero(self.l == layer).squeeze(1)
        if len(sel) == 0:
            return a
        a = a.clone()
        n = self.n[sel]
        T = a.shape[1]
        ar = torch.arange(T, device=a.device)
        cur = a[sel[:, None], ar[None], n[:, None]]
        gate = g[sel[:, None], ar[None], n[:, None]] > 0
        act = (self.s[sel][:, None] * cur > 0) & gate
        a[sel[:, None], ar[None], n[:, None]] = torch.where(act, torch.zeros_like(cur), cur)
        return a


class PoleMean:
    """mlp hook: per row, a set of poles (masks pos (B, L, F) and neg (B, L, F)) is replaced by the neuron's dev mean wherever
    that pole is active, at every position."""

    def __init__(self, mpos, mneg, mean):
        self.mpos, self.mneg, self.mean = mpos, mneg, mean

    def __call__(self, layer, a, g, u):
        mp, mn = self.mpos[:, layer], self.mneg[:, layer]
        if not (mp.any() or mn.any()):
            return a
        open_ = g > 0
        rep = ((a > 0) & open_ & mp[:, None, :]) | ((a < 0) & open_ & mn[:, None, :])
        return torch.where(rep, self.mean[layer].to(a.device)[None, None, :].expand_as(a), a)
