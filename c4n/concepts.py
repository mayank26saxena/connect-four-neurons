"""Exact ground-truth concept labels for Connect Four positions.

All concepts describe the position after t moves (what the model has seen at sequence index t)
from the point of view of the player about to move ("me"); "opp" is the player who just moved.
"""
from __future__ import annotations

import numpy as np

from .engine import H, H1, W, WIN_SCORE, ILLEGAL, bit, playable, replay_boards, winning_cells

ROWS, COLS = range(H), range(W)


def _windows():
    """The 69 four-cell lines: (name, [(row, col) x 4]). Directions: h, v, du (up-right), dd (up-left)."""
    out = []
    for r in ROWS:
        for c in COLS:
            for d, (dr, dc) in (("h", (0, 1)), ("v", (1, 0)), ("du", (1, 1)), ("dd", (1, -1))):
                cells = [(r + k * dr, c + k * dc) for k in range(4)]
                if all(0 <= rr < H and 0 <= cc < W for rr, cc in cells):
                    out.append((f"{d}_r{r}c{c}", cells))
    return out


WINDOWS = _windows()


def _names() -> list[str]:
    n = []
    n += [f"cell_r{r}c{c}_{s}" for r in ROWS for c in COLS for s in ("mine", "theirs", "empty")]
    n += [f"cell_r{r}c{c}_{s}" for r in ROWS for c in COLS for s in ("first", "second")]
    n += [f"land_r{r}c{c}" for r in ROWS for c in COLS]
    n += [f"full_c{c}" for c in COLS]
    n += [f"win_now_c{c}" for c in COLS] + ["win_now_any", "win_now_double"]
    n += [f"block_now_c{c}" for c in COLS] + ["block_now_any", "block_now_double"]
    n += [f"poison_c{c}" for c in COLS]
    n += [f"my_threat_r{r}c{c}" for r in ROWS for c in COLS]
    n += [f"opp_threat_r{r}c{c}" for r in ROWS for c in COLS]
    n += ["my_threats_ge1", "my_threats_ge2", "opp_threats_ge1", "opp_threats_ge2",
          "my_odd_threat", "my_even_threat", "opp_odd_threat", "opp_even_threat"]
    n += [f"last_col_c{c}" for c in COLS]
    n += ["last_made_threat", "last_blocked", "last_stacked"]
    n += [f"ply_{a}_{a + 5}" for a in range(0, 42, 6)]
    n += ["me_first_player"]
    n += ["eval_win", "eval_loss", "eval_ahead", "eval_behind"]
    n += [f"teacher_best_c{c}" for c in COLS]
    n += [f"line_{w}_{who}{k}" for w, _ in WINDOWS for who in ("mine", "theirs") for k in (2, 3)]
    return n


NAMES = _names()
INDEX = {k: i for i, k in enumerate(NAMES)}


def _family(name: str) -> str:
    for pre in ("cell_", "land_", "full_", "win_now", "block_now", "poison_", "my_threat_r", "opp_threat_r",
                "last_col", "ply_", "teacher_best", "line_"):
        if name.startswith(pre):
            return pre.rstrip("_")
    return name.rsplit("_", 0)[0]


FAMILY = [_family(k) for k in NAMES]


def _getbit(x: np.ndarray, c: int, r: int) -> np.ndarray:
    return ((x >> np.uint64(c * H1 + r)) & np.uint64(1)).astype(bool)


def _popcount(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.uint64)
    return np.array([bin(int(v)).count("1") for v in x], dtype=np.int32)


def game_concepts(moves: np.ndarray, scores: np.ndarray) -> np.ndarray:
    """Bool matrix (n, len(NAMES)) for positions t = 0..n-1 of one game.

    `scores` are the teacher's root scores for each position (int16 (n, 7)).
    """
    n = len(moves)
    pos_all, mask_all = replay_boards(moves)
    pos, mask = pos_all[:n], mask_all[:n]
    opp = pos ^ mask
    t = np.arange(n)
    play = playable(mask)
    my_w = winning_cells(pos, mask)
    op_w = winning_cells(opp, mask)
    first = np.where(t % 2 == 0, pos, opp)  # stones of the first player
    second = np.where(t % 2 == 0, opp, pos)

    out = np.zeros((n, len(NAMES)), dtype=bool)

    def setc(name, v):
        out[:, INDEX[name]] = v

    for r in ROWS:
        for c in COLS:
            mi, th, oc = _getbit(pos, c, r), _getbit(opp, c, r), _getbit(mask, c, r)
            setc(f"cell_r{r}c{c}_mine", mi)
            setc(f"cell_r{r}c{c}_theirs", th)
            setc(f"cell_r{r}c{c}_empty", ~oc)
            setc(f"cell_r{r}c{c}_first", _getbit(first, c, r))
            setc(f"cell_r{r}c{c}_second", _getbit(second, c, r))
            setc(f"land_r{r}c{c}", _getbit(play, c, r))
            setc(f"my_threat_r{r}c{c}", _getbit(my_w, c, r))
            setc(f"opp_threat_r{r}c{c}", _getbit(op_w, c, r))

    win_cols = np.zeros((n, W), dtype=bool)
    block_cols = np.zeros((n, W), dtype=bool)
    for c in COLS:
        colmask = np.uint64(((1 << H) - 1) << (c * H1))
        full = _getbit(mask, c, H - 1)
        setc(f"full_c{c}", full)
        win_cols[:, c] = (play & my_w & colmask) != 0
        block_cols[:, c] = (play & op_w & colmask) != 0
        above = ((play & colmask) << np.uint64(1)) & colmask
        setc(f"poison_c{c}", ~full & ((above & op_w) != 0))
        setc(f"win_now_c{c}", win_cols[:, c])
        setc(f"block_now_c{c}", block_cols[:, c])
    setc("win_now_any", win_cols.any(1))
    setc("win_now_double", win_cols.sum(1) >= 2)
    setc("block_now_any", block_cols.any(1))
    setc("block_now_double", block_cols.sum(1) >= 2)

    mc, oc_ = _popcount(my_w), _popcount(op_w)
    setc("my_threats_ge1", mc >= 1)
    setc("my_threats_ge2", mc >= 2)
    setc("opp_threats_ge1", oc_ >= 1)
    setc("opp_threats_ge2", oc_ >= 2)
    odd_rows = np.uint64(sum(1 << (c * H1 + r) for c in COLS for r in (0, 2, 4)))  # rows 1, 3, 5 counted from 1
    even_rows = np.uint64(sum(1 << (c * H1 + r) for c in COLS for r in (1, 3, 5)))
    setc("my_odd_threat", (my_w & odd_rows) != 0)
    setc("my_even_threat", (my_w & even_rows) != 0)
    setc("opp_odd_threat", (op_w & odd_rows) != 0)
    setc("opp_even_threat", (op_w & even_rows) != 0)

    # last move (made by opp, leading into position t)
    if n > 1:
        prev_pos, prev_mask = pos_all[: n - 1], mask_all[: n - 1]  # position t-1, mover there = opp at t
        opp_w_before = winning_cells(prev_pos, prev_mask)       # opp's threats before its move
        me_w_before = winning_cells(prev_pos ^ prev_mask, prev_mask)  # my threats before opp's move
        last_bit = mask[1:] ^ prev_mask
        made = (op_w[1:] & ~opp_w_before) != 0
        blocked = (last_bit & me_w_before) != 0
        lc = moves[: n - 1]
        stacked = np.zeros(n - 1, dtype=bool)
        if n > 2:
            stacked[1:] = moves[1 : n - 1] == moves[: n - 2]
        for c in COLS:
            out[1:, INDEX[f"last_col_c{c}"]] = lc == c
        out[1:, INDEX["last_made_threat"]] = made
        out[1:, INDEX["last_blocked"]] = blocked
        out[1:, INDEX["last_stacked"]] = stacked

    for a in range(0, 42, 6):
        setc(f"ply_{a}_{a + 5}", (t >= a) & (t <= a + 5))
    setc("me_first_player", t % 2 == 0)

    sc = scores.astype(np.int32)
    legal = scores != ILLEGAL
    best = np.where(legal, sc, -10**6).max(1)
    near_win = WIN_SCORE - 43
    setc("eval_win", best >= near_win)
    setc("eval_loss", best <= -near_win)
    setc("eval_ahead", (best > 4) & (best < near_win))
    setc("eval_behind", (best < -4) & (best > -near_win))
    arg = np.where(legal, sc, -10**6).argmax(1)
    for c in COLS:
        setc(f"teacher_best_c{c}", arg == c)
    # four-cell lines: exactly k stones of one side and the rest empty (an open two / open three)
    for w, cells in WINDOWS:
        cm = sum(_getbit(pos, c, r).astype(np.int8) for r, c in cells)
        co = sum(_getbit(opp, c, r).astype(np.int8) for r, c in cells)
        for k in (2, 3):
            setc(f"line_{w}_mine{k}", (cm == k) & (co == 0))
            setc(f"line_{w}_theirs{k}", (co == k) & (cm == 0))
    return out
