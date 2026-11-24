"""Does the model keep a board in its head? Probes for the board state, edits to it, and neuron maps in board terms.

Follows Othello-GPT (Li et al. 2023; Nanda 2023). See PLAN.md addendum (h).

Conventions. Cell k = row * 7 + col, row 0 = bottom. Board states are *relative* (0 empty, 1 mine, 2 theirs; mine = the
player to move at that position) or *absolute* (0 empty, 1 first player, 2 second player). Read points: 0 = after the
embeddings, 2l+1 = after layer l's attention sublayer, 2l+2 = after block l (l = 0..5); 13 in all.
Position t of a game is the residual at token index t (BOS + t moves), which predicts move t.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from . import engine as E
from .model import tokens_from_moves

EMPTY, MINE, THEIRS = 0, 1, 2


def point_names(L=6):
    out = ["embed"]
    for l in range(L):
        out += [f"L{l} attn", f"L{l}"]
    return out


def block_points(L=6):
    """Read points at the block outputs (plus the embeddings): 0, 2, 4, ..., 2L."""
    return [0] + [2 * l + 2 for l in range(L)]


# ---------------------------------------------------------------- labels

def grid42(x):
    return E.bits_to_grid(x).reshape(len(x), 42)


def board_labels(moves, lengths):
    """Per valid position: relative and absolute states (N, 42) int8, threat cells for mover / opponent (N, 42) bool,
    bitboards, move number t and game index g."""
    ps, ms, ts, gs = [], [], [], []
    for g in range(len(lengths)):
        p, m = E.replay_boards(moves[g, : lengths[g]])
        n = int(lengths[g])
        ps.append(p[:n]); ms.append(m[:n]); ts.append(np.arange(n)); gs.append(np.full(n, g))
    pos, mask, t, g = (np.concatenate(a) for a in (ps, ms, ts, gs))
    mine, occ = grid42(pos), grid42(mask)
    rel = np.where(occ, np.where(mine, MINE, THEIRS), EMPTY).astype(np.int8)
    first_to_move = (t % 2 == 0)[:, None]  # the first player is to move at even t
    first = np.where(first_to_move, mine, occ & ~mine)
    ab = np.where(occ, np.where(first, 1, 2), 0).astype(np.int8)
    thr_m = grid42(E.winning_cells(pos, mask))
    thr_t = grid42(E.winning_cells(pos ^ mask, mask))
    return {"rel": rel, "abs": ab, "thr_mine": thr_m, "thr_theirs": thr_t, "pos": pos, "mask": mask, "t": t, "g": g}


# ---------------------------------------------------------------- forward with read / write access to the residual stream

def run(model, tok, resid_hook=None, attn_hook=None, mlp_hook=None, keep=None):
    """Forward pass. resid_hook(point, x) -> x is applied at every read point. keep: read points to return (B, T, d) each."""
    x = model.tok(tok) + model.pos(torch.arange(tok.shape[1], device=tok.device))
    kept = {}

    def at(pt, x):
        if resid_hook is not None:
            x = resid_hook(pt, x)
        if keep is not None and pt in keep:
            kept[pt] = x
        return x

    x = at(0, x)
    for l, b in enumerate(model.blocks):
        x = at(2 * l + 1, x + b.attn(b.n1(x), l, attn_hook))
        x = at(2 * l + 2, x + b.mlp(b.n2(x), l, mlp_hook))
    return model.head(model.nf(x)), kept


@torch.no_grad()
def collect_points(model, moves, lengths, device, points, bs=512, attn_hook=None, mlp_hook=None):
    """Residual stream at the given read points for every valid position: (N, len(points), d) float16 on the CPU."""
    out = []
    for i in range(0, len(lengths), bs):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + bs])).to(device)
        ln = torch.as_tensor(lengths[i:i + bs], device=device)
        valid = torch.arange(42, device=device)[None] < ln[:, None]
        _, kept = run(model, tok, attn_hook=attn_hook, mlp_hook=mlp_hook, keep=set(points))
        out.append(torch.stack([kept[p][:, :42][valid] for p in points], 1).half().cpu())
    return torch.cat(out)


# ---------------------------------------------------------------- probes

class Probe:
    """Linear probe in raw residual coordinates: logits = x @ W + b, W (d, K, C), b (K, C)."""

    def __init__(self, W, b):
        self.W, self.b = W, b

    def logits(self, x):
        d, K, C = self.W.shape
        return (x.float() @ self.W.reshape(d, K * C) + self.b.reshape(-1)).reshape(*x.shape[:-1], K, C)


def fit_linear(X, Y, n_cls, device, steps=500, lr=1e-2, wd=1e-4, seed=0):
    """Multinomial logistic regression per cell. X (N, d) float16 CPU, Y (N, K) int. Full batch Adam on inputs scaled by
    their RMS (folded back into W, so the probe acts on the raw residual)."""
    torch.manual_seed(seed)
    Xt = X.to(device).float()
    s = Xt.pow(2).mean().sqrt()
    Xt = Xt / s
    Yt = torch.as_tensor(Y, device=device).long()
    N, d = Xt.shape
    K = Yt.shape[1]
    W = torch.zeros(d, K * n_cls, device=device, requires_grad=True)
    b = torch.zeros(K * n_cls, device=device, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=lr)
    for _ in range(steps):
        lg = (Xt @ W + b).view(N, K, n_cls)
        loss = F.cross_entropy(lg.reshape(-1, n_cls), Yt.reshape(-1)) + wd * W.pow(2).sum()
        opt.zero_grad(); loss.backward(); opt.step()
    return Probe((W.detach() / s).view(d, K, n_cls), b.detach().view(K, n_cls))


def fit_binary(X, Y, device, steps=500, lr=1e-2, wd=1e-4, seed=0):
    """Independent logistic regressions for K binary targets. Returns (W (d, K), b (K))."""
    torch.manual_seed(seed)
    Xt = X.to(device).float()
    s = Xt.pow(2).mean().sqrt()
    Xt = Xt / s
    Yt = torch.as_tensor(Y, device=device).float()
    W = torch.zeros(Xt.shape[1], Yt.shape[1], device=device, requires_grad=True)
    b = torch.zeros(Yt.shape[1], device=device, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=lr)
    for _ in range(steps):
        loss = F.binary_cross_entropy_with_logits(Xt @ W + b, Yt) + wd * W.pow(2).sum()
        opt.zero_grad(); loss.backward(); opt.step()
    return W.detach() / s, b.detach()


def fit_mlp(X, Y, n_cls, device, hidden=512, steps=800, lr=2e-3, seed=0, bs=8192):
    torch.manual_seed(seed)
    Xt = X.to(device).float()
    s = Xt.pow(2).mean().sqrt()
    Yt = torch.as_tensor(Y, device=device).long()
    K = Yt.shape[1]
    net = torch.nn.Sequential(torch.nn.Linear(Xt.shape[1], hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, K * n_cls)).to(device)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    g = torch.Generator(device="cpu").manual_seed(seed)
    for _ in range(steps):
        idx = torch.randint(0, len(Xt), (bs,), generator=g).to(device)
        loss = F.cross_entropy(net(Xt[idx] / s).view(-1, n_cls), Yt[idx].reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    return lambda x: net(x.float() / s).view(*x.shape[:-1], K, n_cls)


@torch.no_grad()
def predict(fn, X, device, bs=16384):
    return torch.cat([fn(X[i:i + bs].to(device)).argmax(-1).cpu() for i in range(0, len(X), bs)]).numpy()


def board_scores(pred, true):
    """overall accuracy, emptiness accuracy, colour accuracy (on occupied cells; predicting empty counts as wrong)."""
    occ = true != EMPTY
    return {"acc": float((pred == true).mean()),
            "empty_acc": float(((pred == EMPTY) == (true == EMPTY)).mean()),
            "colour_acc": float((pred[occ] == true[occ]).mean())}


def ply_baseline(Y_train, t_train, Y_test, t_test, n_cls=3):
    """Per-cell majority state given the move number (fitted on the training games)."""
    maj = np.zeros((43, Y_train.shape[1]), dtype=np.int8)
    for tt in range(43):
        sel = t_train == tt
        if sel.any():
            cnt = np.stack([(Y_train[sel] == c).sum(0) for c in range(n_cls)])
            maj[tt] = cnt.argmax(0)
    return maj[t_test]


def auroc(score, y):
    pos, neg = score[y], score[~y]
    if len(pos) < 20 or len(neg) < 20:
        return float("nan")
    r = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    return float((r[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


@torch.no_grad()
def margins(probe, X, Y, device, bs=16384):
    """Margin of the true class over the best other class, (N, K)."""
    out = []
    for i in range(0, len(X), bs):
        lg = probe.logits(X[i:i + bs].to(device))
        y = torch.as_tensor(Y[i:i + bs], device=device).long()
        tr = lg.gather(-1, y[..., None])[..., 0]
        other = lg.scatter(-1, y[..., None], -1e9).max(-1).values
        out.append((tr - other).cpu())
    return torch.cat(out).numpy()


# ---------------------------------------------------------------- edits

def edit_alpha(x, W, b, src, tgt, m):
    """Step sizes along u = w_tgt - w_src that make the probe's margin of tgt over every other class equal m.
    x (B, d); W (d, 3) per row given as (B, d, 3); b (B, 3); src, tgt (B,) long; m (B,). Returns alpha (B,), u (B, d)."""
    ar = torch.arange(len(x), device=x.device)
    wt, ws = W[ar, :, tgt], W[ar, :, src]
    u = wt - ws
    lg = torch.einsum("bd,bdc->bc", x, W) + b
    diff0 = lg[ar, tgt][:, None] - lg  # (B, 3): margin of tgt over each class
    slope = torch.einsum("bd,bdc->bc", u, wt[:, :, None] - W)
    need = (m[:, None] - diff0) / slope.clamp_min(1e-12)
    need = torch.where((slope > 1e-12) & (torch.arange(3, device=x.device)[None] != tgt[:, None]), need, torch.full_like(need, -1e9))
    return need.max(1).values.clamp_min(0), u


def edit_hook(probes, rows, cols, cells, src, tgt, m, start, rand=None, only=None):
    """Residual hook that edits the board belief at (rows, cols) at block outputs from layer `start` on (or only at layer
    `only`). probes: {point: Probe}; m: {point: (B,) target margins}. rand: optional (B, d) unit vectors; when given, the
    edit moves along them with the same norm as the probe edit (control)."""
    def hook(pt, x):
        if pt % 2 or pt == 0:
            return x
        l = (pt - 2) // 2
        if (only is not None and l != only) or (only is None and l < start):
            return x
        P = probes[pt]
        xs = x[rows, cols].float()
        Wc, bc = P.W[:, cells].permute(1, 0, 2), P.b[cells]
        a, u = edit_alpha(xs, Wc, bc, src, tgt, m[pt])
        step = a[:, None] * u
        if rand is not None:
            step = rand * step.norm(dim=1, keepdim=True)
        x = x.clone()
        x[rows, cols] = (xs + step).to(x.dtype)
        return x
    return hook


def candidate_edits(pos, mask):
    """All single-cell edits of one board that keep it a legal Connect Four position shape.
    Returns list of (kind, cell, src, tgt, new_pos, new_mask). kind: flip / remove / add."""
    out = []
    mine, occ = grid42(np.array([pos], dtype=np.uint64))[0], grid42(np.array([mask], dtype=np.uint64))[0]
    for c in range(7):
        h = int(occ[[r * 7 + c for r in range(6)]].sum())
        for r in range(h):
            k = r * 7 + c
            bit = int(E.bit(c, r))
            if mine[k]:
                out.append(("flip", k, MINE, THEIRS, pos & ~bit, mask))
            else:
                out.append(("flip", k, THEIRS, MINE, pos | bit, mask))
        if h > 0:
            k = (h - 1) * 7 + c
            bit = int(E.bit(c, h - 1))
            out.append(("remove", k, MINE if mine[k] else THEIRS, EMPTY, pos & ~bit, mask & ~bit))
        if h < 6:
            k = h * 7 + c
            bit = int(E.bit(c, h))
            out.append(("add", k, EMPTY, MINE, pos | bit, mask | bit))
            out.append(("add", k, EMPTY, THEIRS, pos, mask | bit))
    return out


def best_set(scores):
    s = np.asarray(scores).astype(np.int64)
    legal = s != E.ILLEGAL
    mx = s[legal].max()
    return legal & (s == mx)


# ---------------------------------------------------------------- neurons in board terms

def probe_dirs(P):
    """Per cell: mine-minus-theirs and empty-minus-occupied directions (d, 42) each."""
    W = P.W
    return W[:, :, MINE] - W[:, :, THEIRS], W[:, :, EMPTY] - 0.5 * (W[:, :, MINE] + W[:, :, THEIRS])


def cos_map(V, D):
    """V (F, d) neuron vectors, D (d, K) directions -> (F, K) cosines."""
    return F.normalize(V.float(), dim=1) @ F.normalize(D.float(), dim=0)
