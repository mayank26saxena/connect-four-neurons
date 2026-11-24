"""Circuit discovery with minimal pairs (PLAN.md addendum (s)).

A *task* picks clean positions that have one correct column and builds a corrupted twin by changing only the last move. The
two token sequences are identical except for the last token, so in a causal model every activation before the last position is
identical, and patching a component means replacing its output at the last position only. `block_pairs` is the first task
(must-block); another task needs only a function with the same output dict.

Terms. margin = log-sum-exp of the correct column minus log-sum-exp of the other legal columns (`tactics.margin`).
gap = mean margin(clean) - mean margin(corrupted). Noising effect of a patch = (mean margin(clean) - mean margin(clean with the
patched outputs taken from the corrupted run)) / gap. Denoising restoration = (mean margin(corrupted with clean outputs) -
mean margin(corrupted)) / gap.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from . import engine as E
from .model import tokens_from_moves
from .tactics import COLMASK, boards, margin, position_index

ORIENT = ["vertical", "horizontal", "diagonal", "multiple"]
DIRS = {"vertical": [1], "horizontal": [E.H1], "diagonal": [E.H1 + 1, E.H1 - 1]}


# ---------------------------------------------------------------- board facts

def winning_dir(p, mask, d):
    """Empty cells where p completes four along one direction (d = 1 vertical, 7 horizontal, 8 / 6 diagonals)."""
    p = p.astype(np.uint64)
    sh = E._sh
    if d == 1:
        r = sh(p, 1) & sh(p, 2) & sh(p, 3)
    else:
        t = sh(p, d) & sh(p, 2 * d)
        r = (t & sh(p, 3 * d)) | (t & sh(p, -d))
        t = sh(p, -d) & sh(p, -2 * d)
        r |= (t & sh(p, d)) | (t & sh(p, -3 * d))
    return r & (E.BOARD ^ mask.astype(np.uint64))


def facts(pos, mask):
    """legal / immediate win / must-block columns (N, 7) for the player to move (pos = their stones), and the opponent's
    playable winning cells (N,) as bits."""
    play = E.playable(mask)
    my_w = E.winning_cells(pos, mask) & play
    op_w = E.winning_cells(pos ^ mask, mask) & play
    legal = np.stack([(play & m) != 0 for m in COLMASK], 1)
    win = np.stack([(my_w & m) != 0 for m in COLMASK], 1)
    block = np.stack([(op_w & m) != 0 for m in COLMASK], 1)
    return legal, win, block, op_w


# ---------------------------------------------------------------- the block task

def block_positions(moves, lengths, min_stones=4):
    """Flat indices of must-block positions (no immediate win, exactly one blocking column, >= min_stones stones)."""
    pos, mask = boards(moves, lengths)
    g, t = position_index(lengths)
    legal, win, block, op_w = facts(pos, mask)
    sel = ~win.any(1) & (block.sum(1) == 1) & (t >= max(min_stones, 1))
    return np.flatnonzero(sel), dict(pos=pos, mask=mask, g=g, t=t, legal=legal, block=block, op_w=op_w)


def block_pairs(moves, lengths, seed=20261122, max_pairs=4000, min_stones=4):
    """Minimal pairs for the block task. Clean: a must-block position after t moves. Corrupted: the same game with only the
    opponent's last move (move t-1) replaced by another legal column c' such that the result has no must-block, no immediate
    win for either side, and the same legal columns."""
    idx, B = block_positions(moves, lengths, min_stones)
    pos, mask, g, t, legal = B["pos"], B["mask"], B["g"], B["t"], B["legal"]
    pp, pm = pos[idx - 1], mask[idx - 1]  # before the opponent's last move: pp = the opponent's stones
    mover = pm ^ pp
    last = moves[g[idx], t[idx] - 1].astype(np.int64)
    opp_win_prev = E.winning_cells(pp, pm)
    playp = E.playable(pm)
    ok = np.zeros((len(idx), 7), dtype=bool)
    for c in range(7):
        land = playp & COLMASK[c]
        l2, w2, b2, _ = facts(mover, pm | land)
        ok[:, c] = ((land != 0) & (c != last) & ((land & opp_win_prev) == 0) & ~w2.any(1) & ~b2.any(1)
                    & (l2 == legal[idx]).all(1))
    rng = np.random.default_rng(seed)
    alt_all = np.array([rng.choice(np.flatnonzero(r)) if r.any() else -1 for r in ok], dtype=np.int64)
    keep = np.flatnonzero(alt_all >= 0)
    if len(keep) > max_pairs:
        keep = np.sort(rng.choice(keep, max_pairs, replace=False))
    i = idx[keep]
    opp, cell = (pos ^ mask)[i], B["op_w"][i]
    kinds = np.stack([np.any([(winning_dir(opp, mask[i], d) & cell) != 0 for d in ds], 0) for ds in DIRS.values()], 1)
    orient = np.where(kinds.sum(1) > 1, 3, kinds.argmax(1))
    G, T, alt = g[i], t[i], alt_all[keep]
    clean = np.full((len(i), 42), -1, dtype=np.int8)
    for k, (gg, tt) in enumerate(zip(G, T)):
        clean[k, :tt] = moves[gg, :tt]
    corr = clean.copy()
    corr[np.arange(len(i)), T - 1] = alt
    return {"g": G, "t": T, "clean": clean, "corr": corr, "alt": alt, "last": last[keep], "block_col": B["block"][i].argmax(1),
            "legal": legal[i], "orient": orient, "n_candidates": int(len(idx)), "n_with_pair": int((alt_all >= 0).sum())}


def subset(P, m):
    """Pairs restricted to a boolean mask (counts kept from the parent)."""
    return {k: (v[m] if isinstance(v, np.ndarray) else v) for k, v in P.items()}


# ---------------------------------------------------------------- patching

class Patcher:
    """Records last-position neuron activations and head outputs on the clean and corrupted runs of a set of pairs, and
    reruns the model with any of them replaced."""

    def __init__(self, model, P, device, bs=1000):
        self.m, self.dev, self.bs, self.P = model, device, bs, P
        self.N = len(P["t"])
        c = model.cfg
        self.L, self.Fd, self.H = c["n_layer"], c["d_ff"], c["n_head"]
        self.tok = {k: tokens_from_moves(torch.as_tensor(P[k])).to(device) for k in ("clean", "corr")}
        self.t = torch.as_tensor(P["t"], device=device)
        self.good = F.one_hot(torch.as_tensor(P["block_col"]), 7).bool().to(device)
        self.legal = torch.as_tensor(P["legal"], device=device)
        self.acts, self.heads, self.base, self.pick = {}, {}, {}, {}
        for k in ("clean", "corr"):
            self.acts[k], self.heads[k] = self._record(k)
            self.base[k], self.pick[k] = self.run(k, return_pick=True)
        self.gap = float(self.base["clean"].mean() - self.base["corr"].mean())

    def _batches(self):
        for s in range(0, self.N, self.bs):
            sl = slice(s, min(self.N, s + self.bs))
            tt = self.t[sl]
            yield sl, tt, torch.arange(len(tt), device=self.dev)

    @torch.no_grad()
    def _record(self, kind):
        A = torch.zeros(self.N, self.L, self.Fd, device=self.dev)
        Y = None
        for sl, tt, ar in self._batches():
            def hook(l, a, g, u):
                A[sl, l] = a[ar, tt]; return a

            def ahook(l, y):
                nonlocal Y
                if Y is None:
                    Y = torch.zeros(self.N, self.L, y.shape[1], y.shape[3], device=self.dev)
                Y[sl, l] = y.permute(0, 2, 1, 3)[ar, tt]; return y
            self.m(self.tok[kind][sl], hook=hook, attn_hook=ahook)
        return A, Y

    @torch.no_grad()
    def run(self, base, neurons=None, heads=(), src=None, return_pick=False, subspace=None):
        """Margins (N,) of the `base` run ("clean"/"corr") with neurons {layer: LongTensor} and heads [(l, h)] set to their
        values in the `src` run at the last position. subspace {layer: U (F, k), orthonormal columns}: the activation's component
        in span(U) is replaced by the `src` run's, a' = a + (a_src - a) U U^T (PLAN addendum (t))."""
        neurons = {l: ix for l, ix in (neurons or {}).items() if len(ix)}
        subspace = subspace or {}
        heads = list(heads)
        out, picks = [], []
        for sl, tt, ar in self._batches():
            hook = ahook = None
            if neurons or subspace:
                def hook(l, a, g, u, sl=sl, tt=tt, ar=ar):
                    if l not in neurons and l not in subspace:
                        return a
                    a = a.clone()
                    if l in subspace:
                        U = subspace[l]
                        cur = a[ar, tt]
                        a[ar, tt] = cur + ((self.acts[src][sl, l] - cur) @ U) @ U.T
                    if l in neurons:
                        ix = neurons[l]
                        a[ar[:, None], tt[:, None], ix[None, :]] = self.acts[src][sl, l][:, ix]
                    return a
            if heads:
                def ahook(l, y, sl=sl, tt=tt, ar=ar):
                    hs = [h for (ll, h) in heads if ll == l]
                    if not hs:
                        return y
                    y = y.clone()
                    for h in hs:
                        y[ar, h, tt] = self.heads[src][sl, l, h]
                    return y
            lg = self.m(self.tok[base][sl], hook=hook, attn_hook=ahook)[ar, tt]
            out.append(margin(lg, self.good[sl], self.legal[sl]))
            picks.append(lg.masked_fill(~self.legal[sl], -1e9).argmax(-1))
        mg = torch.cat(out).cpu().numpy()
        return (mg, torch.cat(picks).cpu().numpy()) if return_pick else mg

    def effect(self, mg, mask=None):
        """Noising effect of a patched clean run's margins (share of the gap removed), optionally on a subset of pairs."""
        m = slice(None) if mask is None else mask
        c, r = self.base["clean"][m], self.base["corr"][m]
        return float((c.mean() - mg[m].mean()) / (c.mean() - r.mean()))

    def restoration(self, mg, mask=None):
        m = slice(None) if mask is None else mask
        c, r = self.base["clean"][m], self.base["corr"][m]
        return float((mg[m].mean() - r.mean()) / (c.mean() - r.mean()))

    def attribution(self):
        """Attribution patching: first-order estimate of each neuron's noising effect, grad(margin) . (a_corr - a_clean) at
        the last position of the clean run, as a share of the gap. (L, F) numpy."""
        tot = torch.zeros(self.L, self.Fd, device=self.dev)
        for sl, tt, ar in self._batches():
            store = {}

            def hook(l, a, g, u):
                a.retain_grad(); store[l] = a; return a
            with torch.enable_grad():
                lg = self.m(self.tok["clean"][sl], hook=hook)[ar, tt]
                margin(lg, self.good[sl], self.legal[sl]).sum().backward()
            for l, a in store.items():
                tot[l] += (a.grad[ar, tt] * (self.acts["corr"][sl, l] - self.acts["clean"][sl, l])).sum(0)
            self.m.zero_grad(set_to_none=True)
        return (-(tot / self.N) / self.gap).cpu().numpy()


def by_layer(flat_ids, Fd, device):
    d = {}
    for f in flat_ids:
        d.setdefault(int(f) // Fd, []).append(int(f) % Fd)
    return {l: torch.as_tensor(sorted(v), device=device) for l, v in d.items()}


def find_circuit(Pt, n_exact, share, cap):
    """The pre-registered rule: attribution ranking -> exact single-neuron noising of the top n_exact -> sort by exact effect
    (positive only) -> circuit = shortest prefix whose joint noising removes >= share of the gap, capped at `cap`."""
    attr = Pt.attribution()
    top = np.argsort(-attr.ravel())[:n_exact]
    exact, deltas = [], {}
    for f in top:
        mg = Pt.run("clean", neurons=by_layer([f], Pt.Fd, Pt.dev), src="corr")
        exact.append(Pt.effect(mg)); deltas[int(f)] = Pt.base["clean"] - mg
    exact = np.array(exact)
    order = [int(top[i]) for i in np.argsort(-exact) if exact[i] > 0]
    curve, k = [], None
    for j in range(1, min(cap, len(order)) + 1):
        e = Pt.effect(Pt.run("clean", neurons=by_layer(order[:j], Pt.Fd, Pt.dev), src="corr"))
        curve.append(e)
        if k is None and e >= share:
            k = j
            break
    compact = k is not None
    k = k if compact else min(cap, len(order))
    return {"attr": attr, "top": [int(f) for f in top], "exact": {int(f): float(e) for f, e in zip(top, exact)}, "order": order,
            "curve": curve, "k": k, "compact": compact, "circuit": order[:k], "deltas": deltas}


def boot(stat, groups, n, seed):
    """Game-bootstrap 95% interval of stat(index array) over pairs grouped by game."""
    rng = np.random.default_rng(seed)
    ug, inv = np.unique(groups, return_inverse=True)
    members = [np.flatnonzero(inv == j) for j in range(len(ug))]
    vals = []
    for _ in range(n):
        pick = rng.integers(0, len(ug), len(ug))
        vals.append(stat(np.concatenate([members[j] for j in pick])))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
