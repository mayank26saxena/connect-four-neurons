"""ctypes bindings to engine/c4.c plus vectorised numpy bitboard helpers.

Bit layout: bit = col * 7 + row (row 0 = bottom), see engine/c4.c.
"""
from __future__ import annotations

import ctypes
import hashlib
import subprocess
from pathlib import Path

import numpy as np

W, H, H1 = 7, 6, 7
WIN_SCORE = 1000
ILLEGAL = -32768
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "engine" / "c4.c"
BUILD = ROOT / "build"

BOTTOM = np.uint64(0x0000040810204081)
BOARD = np.uint64(0x0000040810204081 * ((1 << H) - 1))


def _lib_path() -> Path:
    digest = hashlib.sha256(SRC.read_bytes()).hexdigest()[:12]
    return BUILD / f"libc4_{digest}.so"


def _load() -> ctypes.CDLL:
    path = _lib_path()
    if not path.exists():
        BUILD.mkdir(exist_ok=True)
        # -ffp-contract=off and no fast-math keep softmax sampling identical across compilers
        subprocess.run(["cc", "-O2", "-ffp-contract=off", "-shared", "-fPIC", str(SRC), "-o", str(path), "-lm"], check=True)
    lib = ctypes.CDLL(str(path))
    i8p = ctypes.POINTER(ctypes.c_int8)
    i16p = ctypes.POINTER(ctypes.c_int16)
    lib.c4_score_moves.argtypes = [i8p, ctypes.c_int, ctypes.c_int, i16p]
    lib.c4_score_moves.restype = ctypes.c_int
    lib.c4_gen_game.argtypes = [ctypes.c_uint64, ctypes.c_int, ctypes.c_double, ctypes.c_int, i8p, i16p, ctypes.POINTER(ctypes.c_int)]
    lib.c4_gen_game.restype = ctypes.c_int
    lib.c4_score_board.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int, i16p]
    lib.c4_score_board.restype = ctypes.c_int
    lib.c4_tt_clear.argtypes = []
    lib.c4_nodes.restype = ctypes.c_longlong
    return lib


_LIB = None


def lib() -> ctypes.CDLL:
    global _LIB
    if _LIB is None:
        _LIB = _load()
    return _LIB


def score_moves(moves, depth: int) -> np.ndarray:
    """Teacher scores (int16[7]) for the position after `moves`; ILLEGAL for full columns."""
    m = np.ascontiguousarray(np.asarray(moves, dtype=np.int8))
    out = np.zeros(W, dtype=np.int16)
    rc = lib().c4_score_moves(m.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)), len(m), depth,
                              out.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)))
    if rc != 0:
        raise ValueError(f"illegal sequence {list(moves)}")
    return out


def score_board(pos, mask, depth: int):
    """Teacher scores (int16[7]) for an arbitrary bitboard (pos = stones of the player to move); None if a four exists."""
    out = np.zeros(W, dtype=np.int16)
    rc = lib().c4_score_board(ctypes.c_uint64(int(pos)), ctypes.c_uint64(int(mask)), depth, out.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)))
    return None if rc != 0 else out


def gen_game(seed: int, depth: int, temp: float, random_plies: int):
    moves = np.zeros(W * H, dtype=np.int8)
    scores = np.zeros((W * H, W), dtype=np.int16)
    res = ctypes.c_int(0)
    n = lib().c4_gen_game(ctypes.c_uint64(seed), depth, temp, random_plies,
                          moves.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
                          scores.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)), ctypes.byref(res))
    return moves[:n].copy(), scores[:n].copy(), res.value


def softmax_targets(scores: np.ndarray, temp: float) -> np.ndarray:
    """Teacher policy from scores (..., 7). Illegal moves get probability 0."""
    s = scores.astype(np.float64)
    legal = scores != ILLEGAL
    s = np.where(legal, s, -np.inf)
    s = (s - s.max(axis=-1, keepdims=True)) / temp
    p = np.exp(s) * legal
    return (p / p.sum(axis=-1, keepdims=True)).astype(np.float32)


# ---------------- numpy bitboards ----------------

def _sh(x, k):
    return (x << np.uint64(k)) if k >= 0 else (x >> np.uint64(-k))


def winning_cells(p: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Vectorised c4_winning_cells: empty cells where p would complete four."""
    p = p.astype(np.uint64)
    r = _sh(p, 1) & _sh(p, 2) & _sh(p, 3)
    for d in (H1, H, H + 2):
        t = _sh(p, d) & _sh(p, 2 * d)
        r |= t & _sh(p, 3 * d)
        r |= t & _sh(p, -d)
        t = _sh(p, -d) & _sh(p, -2 * d)
        r |= t & _sh(p, d)
        r |= t & _sh(p, -3 * d)
    return r & (BOARD ^ mask.astype(np.uint64))


def playable(mask: np.ndarray) -> np.ndarray:
    return (mask.astype(np.uint64) + BOTTOM) & BOARD


def bit(col: int, row: int) -> np.uint64:
    return np.uint64(1 << (col * H1 + row))


def bits_to_grid(x: np.ndarray) -> np.ndarray:
    """(N,) uint64 -> (N, 6, 7) bool grid indexed [row, col], row 0 = bottom."""
    x = x.astype(np.uint64)
    out = np.zeros(x.shape + (H, W), dtype=bool)
    for c in range(W):
        for r in range(H):
            out[..., r, c] = ((x >> np.uint64(c * H1 + r)) & np.uint64(1)).astype(bool)
    return out


def replay_boards(moves: np.ndarray):
    """Bitboards before each move and after the last one.

    Returns (pos, mask) arrays of length n+1 where index t is the position after t moves and
    `pos` holds the stones of the player to move at t.
    """
    n = len(moves)
    pos = np.zeros(n + 1, dtype=np.uint64)
    mask = np.zeros(n + 1, dtype=np.uint64)
    p, m = 0, 0
    for t, c in enumerate(moves):
        p ^= m
        m |= m + (1 << (int(c) * H1))
        pos[t + 1], mask[t + 1] = p, m
    return pos, mask
