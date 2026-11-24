"""Neuron-level analysis primitives: capture, percentiles, ablation hooks, pole-concept matching.

Conventions (following Tigges et al. 2026):
- activation a = SiLU(gate) * up, per neuron and position;
- a neuron has two poles; the positive pole "fires" at a > p_hi, the negative pole at a < p_lo, with per-neuron
  percentiles over the analysis split (default p97 / p3);
- quadrant code q = 2 * [gate > 0] + [up > 0]: 3 = (+,+), 2 = (+,-), 0 = (-,-), 1 = (-,+).
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from . import engine as E
from .model import tokens_from_moves


def valid_index(lengths: np.ndarray):
    """(game, t) pairs for every position at which a move is predicted."""
    g = np.repeat(np.arange(len(lengths)), lengths)
    t = np.concatenate([np.arange(n) for n in lengths])
    return g, t


@torch.no_grad()
def collect_logits(model, moves, lengths, device, batch=2048, hook=None):
    """Logits only (N, 7) for every valid position; no activation copies."""
    out = []
    for i in range(0, len(lengths), batch):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + batch])).to(device)
        ln = torch.as_tensor(lengths[i:i + batch], device=device).long()
        lg = model(tok, hook=hook)[:, :42].float()
        out.append(lg[torch.arange(42, device=device)[None] < ln[:, None]].cpu())
    return torch.cat(out)


@torch.no_grad()
def collect(model, moves, lengths, device, batch=1024, hook=None, want_quad=False):
    """Run the model on whole games; return flat per-position tensors (positions in valid_index order).

    acts  (N, L, F) float16   neuron activations
    quad  (N, L, F) int8      quadrant code
    logits (N, 7) float32
    """
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    N = int(lengths.sum())
    acts = torch.empty((N, L, Fd), dtype=torch.float16)
    quad = torch.empty((N, L, Fd), dtype=torch.int8) if want_quad else None
    logits = torch.empty((N, 7), dtype=torch.float32)
    ptr = 0
    for i in range(0, len(lengths), batch):
        mv = torch.as_tensor(moves[i:i + batch])
        ln = torch.as_tensor(lengths[i:i + batch]).long()
        tok = tokens_from_moves(mv).to(device)
        store = {}

        def rec(layer, a, g, u):
            store[layer] = (a, (2 * (g > 0) + (u > 0)).to(torch.int8))
            return a if hook is None else hook(layer, a, g, u)

        out = model(tok, hook=rec)[:, :42].float()
        valid = (torch.arange(42, device=device)[None] < ln.to(device)[:, None])
        n = int(valid.sum())
        logits[ptr:ptr + n] = out[valid].cpu()
        for l in range(L):
            a, q = store[l]
            acts[ptr:ptr + n, l] = a[:, :42][valid].half().cpu()
            if want_quad:
                quad[ptr:ptr + n, l] = q[:, :42][valid].cpu()
        ptr += n
    return acts, quad, logits


def percentiles(acts: torch.Tensor, qs, device, col_chunk: int = 512) -> torch.Tensor:
    """Per-neuron percentiles: returns (len(qs), L, F) float32 using the nearest-rank on sorted values."""
    N, L, Fd = acts.shape
    out = torch.empty((len(qs), L, Fd))
    for l in range(L):
        for c0 in range(0, Fd, col_chunk):  # sort a block of neurons at a time: bounds GPU memory for wide layers
            s = acts[:, l, c0:c0 + col_chunk].to(device).float().sort(0).values
            for i, q in enumerate(qs):
                k = min(N - 1, max(0, int(round(q / 100 * (N - 1)))))
                out[i, l, c0:c0 + col_chunk] = s[k].cpu()
    return out


# ---------------- hooks ----------------

def band_ablation_hook(lo: torch.Tensor, hi: torch.Tensor):
    """Zero every activation strictly inside (lo, hi) per neuron. lo/hi: (L, F) on the model device."""
    def hook(layer, a, g, u):
        keep = (a <= lo[layer]) | (a >= hi[layer])
        return a * keep
    return hook


def topk_hook(k: int, mode: str = "top", seed: int = 0):
    """Per position and layer keep k neurons: by |a| ('top'), at random ('random'), or drop the top k ('bottom')."""
    gen = torch.Generator().manual_seed(seed)

    def hook(layer, a, g, u):
        if mode == "random":
            r = torch.rand(a.shape, generator=gen).to(a.device)
            idx = r.topk(k, -1).indices
        else:
            idx = a.abs().topk(k, -1).indices
        m = torch.zeros_like(a).scatter_(-1, idx, 1.0)
        return a * (1 - m) if mode == "bottom" else a * m
    return hook


def neuron_hook(layer: int, neuron: int, fn):
    """Apply fn(a_n, g_n, u_n) -> new a_n to one neuron."""
    def hook(l, a, g, u):
        if l != layer:
            return a
        a = a.clone()
        a[..., neuron] = fn(a[..., neuron], g[..., neuron], u[..., neuron])
        return a
    return hook


def compose(*hooks):
    def hook(l, a, g, u):
        for h in hooks:
            a = h(l, a, g, u)
        return a
    return hook


# ---------------- behaviour metrics ----------------

def policy_metrics(logits, ref_logits, scores):
    """KL(ref || logits) over legal moves, and agreement with the teacher's best move. scores: (N, 7) int16."""
    scores = torch.as_tensor(scores)
    legal = scores != E.ILLEGAL
    lp = F.log_softmax(logits.masked_fill(~legal, -1e9), -1)
    lr = F.log_softmax(ref_logits.masked_fill(~legal, -1e9), -1)
    kl = (lr.exp() * (lr - lp)).sum(-1)
    sc = scores.float().masked_fill(~legal, -1e9)
    best = sc.max(-1, keepdim=True).values
    pick = logits.masked_fill(~legal, -1e9).argmax(-1, keepdim=True)
    agree = (sc.gather(-1, pick) == best).float().squeeze(-1)
    return {"kl": kl.mean().item(), "agree": agree.mean().item()}


# ---------------- pole-concept matching ----------------

@torch.no_grad()
def pole_concept_scores(acts, concepts, device, thresholds_pct=(97, 99), sweep_pct=(90, 95, 97, 98, 99, 99.5),
                        min_concept_count=50, rotation=None, chunk=50000, col_chunk=512):
    """F1 between each pole's firing and each binary concept.

    acts: (N, L, F) float16 (CPU); concepts: (N, K) bool numpy. If rotation is given ((L, F, F) orthogonal), activations
    are rotated first (random-direction baseline).
    Returns dict with, per pole (L, F, 2 [pos, neg]):
      f1_at[p]  best-concept F1 when the pole fires beyond percentile p (and its argmax concept index)
      f1_sweep  best F1 over the sweep of firing thresholds (threshold-free strength of the best match)
    """
    N, L, Fd = acts.shape
    C = torch.as_tensor(concepts, dtype=torch.float32)
    ccount = C.sum(0)
    usable = (ccount >= min_concept_count) & (ccount <= N - min_concept_count)
    Cu = C[:, usable].to(device)
    cnt = Cu.sum(0)
    kidx = torch.nonzero(usable).squeeze(1)
    res = {"concept_index": kidx.numpy()}
    all_pct = sorted(set(thresholds_pct) | set(sweep_pct))
    best_at = {p: torch.zeros((L, Fd, 2)) for p in all_pct}
    arg_at = {p: torch.zeros((L, Fd, 2), dtype=torch.long) for p in all_pct}
    for l in range(L):
        Xl = acts[:, l].to(device).float()
        Rl = rotation[l].to(device) if rotation is not None else None
        for c0 in range(0, Fd, col_chunk):  # a block of neurons (or rotated directions) at a time
            Xd = Xl[:, c0:c0 + col_chunk] if Rl is None else Xl @ Rl[:, c0:c0 + col_chunk]
            nc = Xd.shape[1]
            s = Xd.sort(0).values
            for p in all_pct:
                hi = s[min(N - 1, int(round(p / 100 * (N - 1))))]
                lo = s[min(N - 1, int(round((100 - p) / 100 * (N - 1))))]
                for side, fire_fn in ((0, lambda x: x > hi), (1, lambda x: x < lo)):
                    tp = torch.zeros((nc, Cu.shape[1]), device=device)
                    fc = torch.zeros(nc, device=device)
                    for i in range(0, N, chunk):
                        fi = fire_fn(Xd[i:i + chunk]).float()
                        tp += fi.T @ Cu[i:i + chunk]
                        fc += fi.sum(0)
                    f1 = 2 * tp / (fc[:, None] + cnt[None, :]).clamp_min(1)
                    b, a = f1.max(1)
                    best_at[p][l, c0:c0 + nc, side] = b.cpu()
                    arg_at[p][l, c0:c0 + nc, side] = kidx[a.cpu()]
            del Xd, s
        del Xl
    res["f1_at"] = {p: best_at[p].numpy() for p in thresholds_pct}
    res["arg_at"] = {p: arg_at[p].numpy() for p in thresholds_pct}
    stack = torch.stack([best_at[p] for p in sweep_pct])  # (S, L, F, 2)
    b, i = stack.max(0)
    res["f1_sweep"] = b.numpy()
    res["arg_sweep"] = torch.stack([arg_at[p] for p in sweep_pct]).gather(0, i[None]).squeeze(0).numpy()
    res["pct_sweep"] = np.array(sweep_pct)[i.numpy()]
    return res


def random_rotations(L: int, d: int, seed: int, device="cpu") -> torch.Tensor:
    """Haar-random orthogonal matrices (QR of seeded Gaussians, sign-corrected); QR runs on `device`."""
    g = torch.Generator().manual_seed(seed)
    Q = []
    for _ in range(L):
        q, r = torch.linalg.qr(torch.randn(d, d, generator=g, dtype=torch.float64).to(device))
        Q.append((q * torch.sign(torch.diagonal(r))[None]).float().cpu())
    return torch.stack(Q)
