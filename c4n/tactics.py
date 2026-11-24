"""Connect Four tactics as labelled decision problems, plus causal and decoding tools to localise them in the model.

A tactic set holds positions (flat indices into the analysis positions) with masks over the 7 columns:
  good: columns that carry out the tactic        bad: columns that violate it
Tactics (each set excludes positions that belong to a higher-priority tactic, so a position tests one thing):
  win     a winning move exists                      good = winning columns
  block   no win, the opponent threatens to win       good = the blocking column(s)
  poison  no win, no block needed, some legal column lets the opponent win on top   bad = poisoned columns
  fork    no win, no block, a move makes two playable winning cells and the opponent has no immediate win  good = fork columns
Rate = share of positions where the model's greedy legal move is in `good` (or, for poison, not in `bad`).
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from . import engine as E
from .model import tokens_from_moves

H1 = E.H1
COLMASK = [np.uint64(((1 << E.H) - 1) << (c * H1)) for c in range(E.W)]
TACTICS = ["win", "block", "poison", "fork"]


def boards(moves, lengths):
    """pos (stones of the player to move), mask, for every position of every game (flat, valid positions only)."""
    ps, ms = [], []
    for g in range(len(lengths)):
        p, m = E.replay_boards(moves[g, : lengths[g]])
        ps.append(p[: lengths[g]]); ms.append(m[: lengths[g]])
    return np.concatenate(ps), np.concatenate(ms)


def tactic_masks(pos, mask):
    """Boolean (N, 7) arrays: win, block, poison, fork (fork already restricted to positions with no win and no block)."""
    N = len(pos)
    opp = pos ^ mask
    play = E.playable(mask)
    my_w, op_w = E.winning_cells(pos, mask), E.winning_cells(opp, mask)
    win, block, poison, fork = (np.zeros((N, 7), dtype=bool) for _ in range(4))
    legal = np.zeros((N, 7), dtype=bool)
    for c in range(7):
        cm = COLMASK[c]
        land = play & cm
        legal[:, c] = land != 0
        win[:, c] = (land & my_w) != 0
        block[:, c] = (land & op_w) != 0
        above = (land << np.uint64(1)) & cm
        poison[:, c] = legal[:, c] & ((above & op_w) != 0) & ~win[:, c]  # a winning move is never poison
    any_win, any_block = win.any(1), block.any(1)
    for c in range(7):  # fork: after my move at c, I have >= 2 playable winning cells and the opponent has none
        land = play & COLMASK[c]
        pos2 = pos | land
        mask2 = mask | land
        mine2 = E.winning_cells(pos2, mask2) & E.playable(mask2)
        theirs2 = E.winning_cells(mask2 ^ pos2, mask2) & E.playable(mask2)
        two = np.array([bin(int(v)).count("1") >= 2 for v in mine2])
        fork[:, c] = legal[:, c] & two & (theirs2 == 0) & ~any_win & ~any_block
    return {"win": win, "block": block, "poison": poison, "fork": fork, "legal": legal}


def tactic_sets(moves, lengths, max_per_tactic=4000, seed=0):
    pos, mask = boards(moves, lengths)
    m = tactic_masks(pos, mask)
    any_win, any_block = m["win"].any(1), m["block"].any(1)
    sel = {"win": any_win,
           "block": ~any_win & any_block & (m["block"].sum(1) == 1),
           "poison": ~any_win & ~any_block & m["poison"].any(1) & (m["poison"].sum(1) < m["legal"].sum(1)),
           "fork": m["fork"].any(1)}
    rng = np.random.default_rng(seed)
    g_all, t_all = position_index(lengths)
    out = {}
    for t in TACTICS:
        idx = np.flatnonzero(sel[t])
        n_all = len(idx)
        if len(idx) > max_per_tactic:
            idx = np.sort(rng.choice(idx, max_per_tactic, replace=False))
        good = m[t][idx] if t != "poison" else m["legal"][idx] & ~m["poison"][idx]
        bad = m["poison"][idx] if t == "poison" else m["legal"][idx] & ~good
        out[t] = {"idx": idx, "good": good, "bad": bad, "legal": m["legal"][idx], "n_all": n_all, "_g": g_all, "_t": t_all}
    return out


def control_set(moves, lengths, scores, max_n=3000, seed=0):
    """Control task: random positions, correct = any legal column tied for the teacher's best score. Used to separate damage
    that is specific to a tactic from damage that hurts the model in general."""
    g, t = position_index(lengths)
    fs = scores[g, t]
    legal = fs != E.ILLEGAL
    best = np.where(legal, fs, -32768).max(1)
    good = legal & (fs == best[:, None])
    idx = np.sort(np.random.default_rng(seed).choice(len(g), min(max_n, len(g)), replace=False))
    return {"idx": idx, "good": good[idx], "bad": legal[idx] & ~good[idx], "legal": legal[idx], "n_all": len(g), "_g": g, "_t": t}


def _gather(moves, gid, tpos, device):
    """Batch of (game, t) positions -> tokens for the unique games and the row/col to read logits from."""
    ug, inv = np.unique(gid, return_inverse=True)
    tok = tokens_from_moves(torch.as_tensor(moves[ug])).to(device)
    return tok, torch.as_tensor(inv, device=device), torch.as_tensor(tpos, device=device)


def position_index(lengths):
    g = np.repeat(np.arange(len(lengths)), lengths)
    t = np.concatenate([np.arange(n) for n in lengths])
    return g, t


@torch.no_grad()
def rate(model, moves, gt, device, hook=None, attn_hook=None, bs=512):
    """Share of positions of a tactic set where the model's greedy legal move is in `good`."""
    hits, n = 0, len(gt["idx"])
    for i in range(0, n, bs):
        sl = slice(i, i + bs)
        tok, row, col = _gather(moves, gt["_g"][gt["idx"][sl]], gt["_t"][gt["idx"][sl]], device)
        lg = model(tok, hook=hook, attn_hook=attn_hook)[row, col]
        legal = torch.as_tensor(gt["legal"][sl], device=device)
        good = torch.as_tensor(gt["good"][sl], device=device)
        pick = lg.masked_fill(~legal, -1e9).argmax(-1)
        hits += good.gather(1, pick[:, None]).sum().item()
    return hits / max(1, n)


@torch.no_grad()
def good_prob(model, moves, gt, device, hook=None, attn_hook=None, bs=512):
    """Per position: probability mass on the correct columns (softmax over legal moves) and whether the greedy legal move is correct."""
    ps, oks = [], []
    for i in range(0, len(gt["idx"]), bs):
        sl = slice(i, i + bs)
        tok, row, col = _gather(moves, gt["_g"][gt["idx"][sl]], gt["_t"][gt["idx"][sl]], device)
        lg = model(tok, hook=hook, attn_hook=attn_hook)[row, col]
        legal = torch.as_tensor(gt["legal"][sl], device=device)
        good = torch.as_tensor(gt["good"][sl], device=device)
        p = torch.softmax(lg.masked_fill(~legal, -1e9), -1)
        ps.append((p * good).sum(-1).cpu()); oks.append(good.gather(1, lg.masked_fill(~legal, -1e9).argmax(-1)[:, None]).squeeze(1).cpu())
    return torch.cat(ps).numpy(), torch.cat(oks).numpy()


def chance_rate(gt):
    """Expected rate of a player choosing a legal column uniformly at random."""
    return float((gt["good"].sum(1) / gt["legal"].sum(1)).mean())


def margin(logits, good, legal):
    """log-sum-exp of the correct columns minus log-sum-exp of the other legal columns (higher = more of the tactic)."""
    neg = -1e9
    return torch.logsumexp(logits.masked_fill(~good, neg), -1) - torch.logsumexp(logits.masked_fill(~(legal & ~good), neg), -1)


def attribution(model, moves, gt, device, bs=256):
    """Per-neuron first-order effect of zeroing on the tactic margin: sum over positions of a * d(margin)/da.
    Positive = the neuron supports the tactic. Returns (L, F) float32 sums and the number of positions."""
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    tot = torch.zeros(L, Fd, device=device)
    n = len(gt["idx"])
    for i in range(0, n, bs):
        sl = slice(i, i + bs)
        tok, row, col = _gather(moves, gt["_g"][gt["idx"][sl]], gt["_t"][gt["idx"][sl]], device)
        store = {}

        def hook(l, a, g, u):
            a.retain_grad(); store[l] = a
            return a

        with torch.enable_grad():
            lg = model(tok, hook=hook)[row, col]
            good = torch.as_tensor(gt["good"][sl], device=device)
            legal = torch.as_tensor(gt["legal"][sl], device=device)
            m = margin(lg, good, legal)
            m.sum().backward()
        for l in range(L):
            a = store[l]
            tot[l] += (a * a.grad)[row, col].sum(0).detach()
        model.zero_grad(set_to_none=True)
    return tot.cpu().numpy(), n


@torch.no_grad()
def means(model, moves, lengths, device, bs=512):
    """Mean neuron activation (L, F) and mean head output (L, H, dh) over valid positions (for mean-ablation)."""
    L, Fd, Hh = model.cfg["n_layer"], model.cfg["d_ff"], model.cfg["n_head"]
    dh = model.cfg["d_model"] // Hh
    a_sum = torch.zeros(L, Fd, device=device)
    y_sum = torch.zeros(L, Hh, dh, device=device)
    cnt = 0
    for i in range(0, len(lengths), bs):
        mv, ln = moves[i:i + bs], torch.as_tensor(lengths[i:i + bs], device=device)
        tok = tokens_from_moves(torch.as_tensor(mv)).to(device)
        valid = (torch.arange(42, device=device)[None] < ln[:, None])  # positions 0..41 predict moves
        cnt += int(valid.sum())

        def hook(l, a, g, u):
            a_sum[l] += a[:, :42][valid].sum(0); return a

        def ahook(l, y):
            y_sum[l] += y[:, :, :42].permute(0, 2, 1, 3)[valid].sum(0); return y

        model(tok, hook=hook, attn_hook=ahook)
    return (a_sum / cnt).cpu(), (y_sum / cnt).cpu()


def mlp_mean_hook(layer, mean_a):
    m = mean_a[layer]

    def hook(l, a, g, u):
        return m.to(a.device).expand_as(a).clone() if l == layer else a
    return hook


def head_mean_hook(layer, head, mean_y):
    mv = mean_y[layer, head]

    def hook(l, y):
        if l != layer:
            return y
        y = y.clone()
        y[:, head] = mv.to(y.device)[None, None, :]
        return y
    return hook


def neuron_zero_hook(neurons_by_layer):
    idx = {l: torch.as_tensor(n) for l, n in neurons_by_layer.items() if len(n)}

    def hook(l, a, g, u):
        if l not in idx:
            return a
        a = a.clone(); a[..., idx[l].to(a.device)] = 0.0
        return a
    return hook


@torch.no_grad()
def residuals(model, moves, lengths, device, bs=512):
    """Residual stream after the embeddings and after each block at every valid position: (N, L+1, d) float16 (CPU)."""
    out = []
    for i in range(0, len(lengths), bs):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + bs])).to(device)
        ln = torch.as_tensor(lengths[i:i + bs], device=device)
        valid = (torch.arange(42, device=device)[None] < ln[:, None])
        x = model.tok(tok) + model.pos(torch.arange(tok.shape[1], device=device))
        rs = [x[:, :42][valid]]
        for li, b in enumerate(model.blocks):
            x = b(x, li)
            rs.append(x[:, :42][valid])
        out.append(torch.stack(rs, 1).half().cpu())
    return torch.cat(out)


def probe_auroc(X, y, train_mask, device, steps=300, lr=5e-3):
    """Linear probe (logistic regression) on X (N, d); returns held-out AUROC."""
    Xt = X[train_mask].to(device).float(); yt = torch.as_tensor(y[train_mask], device=device).float()
    Xv = X[~train_mask].to(device).float(); yv = y[~train_mask]
    mu, sd = Xt.mean(0), Xt.std(0).clamp_min(1e-4)
    w = torch.zeros(X.shape[1], device=device, requires_grad=True); b = torch.zeros(1, device=device, requires_grad=True)
    opt = torch.optim.Adam([w, b], lr=lr)
    for _ in range(steps):
        loss = F.binary_cross_entropy_with_logits(((Xt - mu) / sd) @ w + b, yt)
        opt.zero_grad(); loss.backward(); opt.step()
    s = (((Xv - mu) / sd) @ w + b).detach().cpu().numpy()
    pos, neg = s[yv == 1], s[yv == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    return float((ranks[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


@torch.no_grad()
def attention_profile(model, moves, gt, device, max_offset=8):
    """Average attention from the deciding position, by offset (0 = the last move played, 1 = the one before, ...) and to
    the start token, for every (layer, head). Returns (L, H, max_offset + 1): offsets 0..max_offset-1, then BOS."""
    L, Hh = model.cfg["n_layer"], model.cfg["n_head"]
    prof = torch.zeros(L, Hh, max_offset + 1, device=device)
    n = len(gt["idx"])
    for i in range(0, n, 256):
        sl = slice(i, i + 256)
        tok, row, col = _gather(moves, gt["_g"][gt["idx"][sl]], gt["_t"][gt["idx"][sl]], device)
        x = model.tok(tok) + model.pos(torch.arange(tok.shape[1], device=device))
        for li, b in enumerate(model.blocks):
            h = b.n1(x)
            B_, T, D = h.shape
            q, k, v = b.attn.qkv(h).view(B_, T, 3, Hh, D // Hh).permute(2, 0, 3, 1, 4)
            att = torch.softmax((q @ k.transpose(-1, -2)) / (D // Hh) ** 0.5 + torch.triu(torch.full((T, T), -1e9, device=device), 1), -1)
            a = att[row[:, None], torch.arange(Hh, device=device)[None, :], col[:, None]]  # (positions, H, T)
            npos = row.shape[0]
            for o in range(max_offset):
                idx = (col - o).clamp_min(0)
                prof[li, :, o] += (a[torch.arange(npos, device=device), :, idx] * (col >= o)[:, None]).sum(0)
            prof[li, :, max_offset] += a[:, :, 0].sum(0)
            x = b(x, li)
    return (prof / n).cpu().numpy()
