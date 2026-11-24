"""Neuron Scientist: agent-written, verified descriptions of units (PLAN.md addendum (q)).

A *unit* is a neuron pole (layer, neuron, sign) or, as a blinded control, a random direction in one layer's neuron space.
Every unit is read the same way: s = a . r, where a is the layer's activation vector (SiLU(gate) * up) at a position and r is a
unit vector (a basis vector for a real neuron). The *pole activation* is sign * s; the unit *fires* when the pole activation is
beyond its dev threshold (p97 of s for a positive pole, p3 for a negative one).

Splits: dev = analysis split (the agent's tools read only this); test = validation split (verification only).
Descriptions are English text plus a program over a `Board` (see `Board`), so detection is scored exactly.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from . import config
from . import engine as E
from .model import C4Transformer, tokens_from_moves

ROOT = config.ROOT
NS = Path(os.environ.get("NS_DIR", ROOT / "ns"))  # NS_DIR redirects the workspace (smoke tests)
PRIVATE = NS / "private"
CACHE = NS / "cache"
EMPTY, MINE, THEIRS = 0, 1, 2
DEV_SPLIT, TEST_SPLIT = "analysis", "val"


# ---------------------------------------------------------------- model and data

def load_web_model(device="cpu") -> C4Transformer:
    """The main model from its float16 web export (web/model.json + model.bin); weights are cast to float32."""
    man = json.loads((ROOT / "web" / "model.json").read_text())
    raw = (ROOT / "web" / man["weights"]).read_bytes()
    sd = {}
    for name, meta in man["tensors"].items():
        n = int(np.prod(meta["shape"]))
        sd[name] = torch.from_numpy(np.frombuffer(raw, dtype=np.float16, count=n, offset=meta["offset"]).astype(np.float32).reshape(meta["shape"]))
    m = C4Transformer(**man["config"])
    m.load_state_dict(sd)
    return m.to(device).eval()


def load_games(split, n_games=5000):
    d = np.load(ROOT / "data" / f"{split}.npz")
    return d["moves"][:n_games], d["scores"][:n_games], d["lengths"][:n_games].astype(np.int64)


def positions(moves, lengths):
    """Flat index of valid positions, game-major: (g, t) with t = number of moves played (0..length-1)."""
    g = np.concatenate([np.full(int(n), i) for i, n in enumerate(lengths)])  # moves is unused (kept for the signature)
    t = np.concatenate([np.arange(int(n)) for n in lengths])
    return g, t


# ---------------------------------------------------------------- boards

class BoardSet:
    """Precomputed facts for every position of a set of games (vectorised); `board(i)` gives a `Board` view."""

    def __init__(self, moves, lengths):
        self.moves, self.lengths = moves, lengths
        self.g, self.t = positions(moves, lengths)
        ps, ms = [], []
        for i, n in enumerate(lengths):
            p, m = E.replay_boards(moves[i, : int(n)])
            ps.append(p[: int(n)]); ms.append(m[: int(n)])
        self.pos, self.mask = np.concatenate(ps), np.concatenate(ms)
        mine, occ = E.bits_to_grid(self.pos), E.bits_to_grid(self.mask)       # (N, 6, 7), row 0 = bottom
        self.grid = np.where(occ, np.where(mine, MINE, THEIRS), EMPTY).astype(np.int8)
        self.heights = occ.sum(1).astype(np.int8)                              # (N, 7)
        play = E.playable(self.mask)
        self.mine_wins = E.bits_to_grid(E.winning_cells(self.pos, self.mask))
        self.theirs_wins = E.bits_to_grid(E.winning_cells(self.pos ^ self.mask, self.mask))
        self.playable = E.bits_to_grid(play)
        self.last_col = np.where(self.t > 0, self.moves[self.g, np.maximum(self.t - 1, 0)], -1).astype(np.int8)

    def __len__(self):
        return len(self.g)

    def board(self, i):
        return Board(self, i)


class Board:
    """The position the model has just read, from the point of view of the player about to move ("me").

    grid[r][c]      0 empty, 1 mine, 2 theirs; r = 0 is the bottom row, c = 0 the leftmost column (columns are 0-6)
    heights[c]      stones in column c;  landing(c) -> row where a stone dropped in c lands, or None if full
    legal           list of playable columns
    last_col, last_row   where the last stone went (None at the start); ply = stones on the board
    me_first        True if "me" is the first player
    my_wins / their_wins             set of empty (r, c) cells that would complete four for me / the opponent
    my_playable_wins / their_playable_wins   the subset that are landing cells right now (an immediate win / a must-block)
    moves           the game so far, as a list of columns
    """

    __slots__ = ("grid", "heights", "legal", "last_col", "last_row", "ply", "me_first", "my_wins", "their_wins",
                 "my_playable_wins", "their_playable_wins", "moves")

    def __init__(self, bs: BoardSet, i: int):
        g, t = bs.g[i], int(bs.t[i])
        self.grid = bs.grid[i].tolist()
        self.heights = bs.heights[i].tolist()
        self.legal = [c for c in range(7) if self.heights[c] < 6]
        self.ply = t
        self.me_first = t % 2 == 0
        self.moves = bs.moves[g, :t].tolist()
        self.last_col = int(bs.last_col[i]) if t > 0 else None
        self.last_row = self.heights[self.last_col] - 1 if t > 0 else None
        cells = lambda a: {(r, c) for r in range(6) for c in range(7) if a[r, c]}
        self.my_wins, self.their_wins = cells(bs.mine_wins[i]), cells(bs.theirs_wins[i])
        self.my_playable_wins = {x for x in self.my_wins if bs.playable[i][x]}
        self.their_playable_wins = {x for x in self.their_wins if bs.playable[i][x]}

    def landing(self, c):
        return self.heights[c] if self.heights[c] < 6 else None

    def render(self):
        rows = ["".join(".XO"[self.grid[r][c]] for c in range(7)) for r in range(5, -1, -1)]
        return "\n".join(rows) + "\n0123456   X = me (to move), O = them"


def board_from_moves(moves):
    """Board after `moves` (a list of columns). A placeholder move is appended so the final position is included."""
    moves = list(moves)
    if len(moves) >= 42:
        raise ValueError("the board is full")
    h = [moves.count(c) for c in range(7)]
    mv = np.full((1, 42), -1, dtype=np.int8)
    mv[0, : len(moves) + 1] = moves + [next(c for c in range(7) if h[c] < 6)]
    return BoardSet(mv, np.array([len(moves) + 1])).board(len(moves))


# ---------------------------------------------------------------- programs written by the agent

SAFE = {k: __builtins__[k] if isinstance(__builtins__, dict) else getattr(__builtins__, k) for k in
        ("abs", "all", "any", "bool", "dict", "enumerate", "float", "int", "len", "list", "max", "min", "range", "round",
         "set", "sorted", "sum", "tuple", "zip", "reversed")}


def load_program(code: str):
    """Compile an agent program. It must define `fires(b) -> bool|float` and may define `level(b) -> int 0-9` (used for
    simulation; defaults to fires). No imports; only basic builtins."""
    if "import" in code or "__" in code or "open(" in code or "exec(" in code or "eval(" in code:
        raise ValueError("programs may not import, open files, exec or use dunder names")
    ns = {"__builtins__": SAFE}
    exec(compile(code, "<agent program>", "exec"), ns)
    if "fires" not in ns:
        raise ValueError("program must define fires(b)")
    return ns["fires"], ns.get("level")


def run_program(fn, bs: BoardSet, idx=None):
    idx = range(len(bs)) if idx is None else idx
    return np.array([float(fn(bs.board(int(i)))) for i in idx], dtype=np.float64)


# ---------------------------------------------------------------- units and activations

def units():
    return json.loads((NS / "units.json").read_text())


def unit_key():
    """Private: maps unit id -> kind / neuron / direction. Read by the tools and verification, never shown to the agent."""
    return json.loads((PRIVATE / "key.json").read_text())


def unit_vector(u, key, d_ff):
    k = key[u]
    if k["kind"] == "neuron":
        r = torch.zeros(d_ff); r[k["neuron"]] = 1.0
    else:
        g = torch.Generator().manual_seed(int(k["seed"]))
        r = F.normalize(torch.randn(d_ff, generator=g), dim=0)
    return r


@torch.no_grad()
def unit_acts(model, moves, lengths, us, key, bs=512):
    """(N, len(us)) raw unit activations s = a . r at every valid position, in one pass over the games."""
    d_ff = model.cfg["d_ff"]
    by_layer = {}
    for j, u in enumerate(us):
        by_layer.setdefault(key[u]["layer"], []).append(j)
    R = {l: torch.stack([unit_vector(us[j], key, d_ff) for j in js], 1) for l, js in by_layer.items()}
    out = []
    for i in range(0, len(lengths), bs):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + bs]))
        valid = torch.arange(42)[None] < torch.as_tensor(lengths[i:i + bs])[:, None]
        cols = torch.zeros(int(valid.sum()), len(us))

        def hook(l, a, g, u):
            if l in R:
                cols[:, by_layer[l]] = a[:, :42][valid].float() @ R[l]
            return a
        model(tok, hook=hook)
        out.append(cols)
    return torch.cat(out).numpy()


@torch.no_grad()
def acts_for_sequence(model, moves, u, key):
    """Raw activation of unit u at every position of one game (position t = after t moves)."""
    mv = np.full((1, 42), -1, dtype=np.int8); mv[0, : len(moves)] = moves
    n = min(len(moves) + 1, 42)
    s = unit_acts(model, mv, np.array([n]), [u], key)[:, 0]
    return s


@torch.no_grad()
def move_probs(model, moves, u=None, key=None, value=None):
    """Move probabilities after `moves`; with u and value, the unit's activation is set to `value` (raw s) at the last position."""
    tok = tokens_from_moves(torch.as_tensor(np.array([list(moves) + [-1] * (42 - len(moves))], dtype=np.int8)))
    t = len(moves)
    hook = None
    if u is not None:
        layer, r = key[u]["layer"], unit_vector(u, key, model.cfg["d_ff"])

        def hook(l, a, g, uu):
            if l != layer:
                return a
            a = a.clone()
            s = a[0, t] @ r
            a[0, t] = a[0, t] + (value - s) * r
            return a
    lg = model(tok, hook=hook)[0, t]
    legal = torch.as_tensor([sum(1 for m in moves if m == c) < 6 for c in range(7)])
    return torch.softmax(lg.masked_fill(~legal, -1e9), -1).numpy()


# ---------------------------------------------------------------- scores

def f1(pred, fire):
    tp = float((pred & fire).sum())
    return 2 * tp / max(1.0, float(pred.sum() + fire.sum())), tp / max(1.0, float(pred.sum())), tp / max(1.0, float(fire.sum()))


def auroc(score, y):
    pos, neg = score[y], score[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = np.argsort(np.argsort(np.concatenate([pos, neg]), kind="stable"), kind="stable") + 1.0
    # average ranks for ties
    allv = np.concatenate([pos, neg])
    _, inv, cnt = np.unique(allv, return_inverse=True, return_counts=True)
    sums = np.zeros(len(cnt)); np.add.at(sums, inv, r)
    r = (sums / cnt)[inv]
    return float((r[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def level_map(level_fit, s_fit, n_bins=10):
    """Map program levels to mean raw activation (fitted on one sample): returns (keys, means) for lookup."""
    lv = np.asarray(level_fit, dtype=np.float64)
    if len(lv) == 0:
        raise ValueError("level_map needs at least one fitting position")
    vals = np.unique(lv)
    if len(vals) > n_bins:  # continuous: quantile bins
        edges = np.unique(np.quantile(lv, np.linspace(0, 1, n_bins + 1)[1:-1]))
        b = np.searchsorted(edges, lv, side="right")
        means = np.array([s_fit[b == k].mean() if (b == k).any() else s_fit.mean() for k in range(len(edges) + 1)])
        return ("bins", edges, means)
    means = np.array([s_fit[lv == v].mean() for v in vals])
    return ("values", vals, means)


def apply_level_map(m, level):
    kind, keys, means = m
    lv = np.asarray(level, dtype=np.float64)
    if kind == "bins":
        return means[np.searchsorted(keys, lv, side="right")]
    idx = np.clip(np.searchsorted(keys, lv), 0, len(keys) - 1)
    exact = keys[idx] == lv
    return np.where(exact, means[idx], means.mean())


@torch.no_grad()
def kl_recovery(model, moves, lengths, u, key, sim, s_true):
    """Replace unit u's activation at every valid position by `sim` (flat, game-major). Returns KL(intact||sim),
    KL(intact||zero) averaged over positions, and recovery = 1 - KL_sim / KL_zero."""
    layer, r = key[u]["layer"], unit_vector(u, key, model.cfg["d_ff"])
    out = {"sim": 0.0, "zero": 0.0}
    n_tot = 0
    ptr = 0
    for i in range(0, len(lengths), 512):
        mv, ln = moves[i:i + 512], torch.as_tensor(lengths[i:i + 512])
        tok = tokens_from_moves(torch.as_tensor(mv))
        valid = torch.arange(42)[None] < ln[:, None]
        n = int(valid.sum())
        base = F.log_softmax(model(tok)[:, :42][valid], -1)
        for name, target in (("sim", torch.as_tensor(sim[ptr:ptr + n], dtype=torch.float32)), ("zero", torch.zeros(n))):
            def hook(l, a, g, uu, target=target):
                if l != layer:
                    return a
                a = a.clone()
                sub = a[:, :42][valid]
                sub = sub + (target - sub @ r)[:, None] * r[None]
                a42 = a[:, :42].clone(); a42[valid] = sub
                a[:, :42] = a42
                return a
            lp = F.log_softmax(model(tok, hook=hook)[:, :42][valid], -1)
            out[name] += float((base.exp() * (base - lp)).sum())
        ptr += n; n_tot += n
    ks, kz = out["sim"] / n_tot, out["zero"] / n_tot
    return {"kl_sim": ks, "kl_zero": kz, "recovery": 1 - ks / kz if kz > 0 else float("nan")}


def ns_config(cfg):
    """The neuron_scientist config, with NS_GAMES (smoke runs) capping every game count."""
    nc = dict(cfg["neuron_scientist"])
    nc.setdefault("min_ply", 0)        # (r) positions with ply < min_ply are ineligible: no threshold, detection or judge use
    nc.setdefault("exclude_key", None)
    nc.setdefault("study", "q")         # "r": NaN-safe medians and the r_f random-null test in verification  # (r) a previous study's key: its neurons are not sampled again
    if os.environ.get("NS_GAMES"):
        g = int(os.environ["NS_GAMES"])
        caps = {"n_games": g, "dev_score_games": g // 2, "dev_sim_games": g // 4, "test_sim_games": g // 2, "fit_games": g // 2}
        for k, v in caps.items():
            nc[k] = min(nc[k], max(2, v))
    return nc


def eligible(lengths, min_ply):
    """(r) Boolean mask over flat positions (game-major): True where ply >= min_ply. Every game starts from the same few
    openings, so a direction that happens to be extreme on one of them would 'fire' there and get a trivially exact rule."""
    _, t = positions(None, lengths)
    return t >= min_ply


def stats():
    return json.loads((NS / "stats.json").read_text())


def fires_from(s, st, u):
    """Boolean firing of unit u given raw activations s and the dev stats."""
    z = st[u]
    return (s > z["thr"]) if z["sign"] > 0 else (s < z["thr"])
