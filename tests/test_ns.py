"""Neuron Scientist core: boards agree with the engine, programs are sandboxed, unit reads/writes are consistent."""
import numpy as np
import pytest
import torch

from c4n import engine as E
from c4n import ns


def test_board_matches_engine():
    mv = E.gen_game(7, 4, 1.0, 4)[0][:15].tolist()
    b = ns.board_from_moves(mv)
    p, m = E.replay_boards(np.array(mv, dtype=np.int8))
    assert b.ply == len(mv) and sum(b.heights) == len(mv)
    mine = E.bits_to_grid(p[-1:])[0]
    assert all((b.grid[r][c] == ns.MINE) == bool(mine[r, c]) for r in range(6) for c in range(7))
    assert b.last_col == mv[-1] and b.grid[b.last_row][b.last_col] == ns.THEIRS  # the last stone belongs to the opponent
    win = E.bits_to_grid(E.winning_cells(p[-1:], m[-1:]))[0]
    assert b.my_wins == {(r, c) for r in range(6) for c in range(7) if win[r, c]}


def test_program_sandbox():
    f, lv = ns.load_program("def fires(b):\n    return b.heights[3] >= 2\n")
    assert lv is None and f(ns.board_from_moves([3, 3])) and not f(ns.board_from_moves([3]))
    for bad in ("import os\ndef fires(b): return 1", "def fires(b): return open('x')", "def fires(b): return b.__class__"):
        with pytest.raises(ValueError):
            ns.load_program(bad)


def test_scores():
    y = np.array([1, 1, 0, 0, 0], bool)
    assert ns.f1(y, y)[0] == 1.0 and ns.auroc(np.array([.9, .8, .1, .2, .3]), y) == 1.0
    assert abs(ns.auroc(np.ones(5), y) - 0.5) < 1e-9
    m = ns.level_map(np.array([0, 0, 1, 1]), np.array([1., 3., 10., 20.]))
    assert np.allclose(ns.apply_level_map(m, np.array([0, 1])), [2., 15.])


def test_unit_reads_and_steering():
    model = ns.load_web_model()
    key = {"A": {"kind": "neuron", "layer": 2, "neuron": 5}, "B": {"kind": "random_direction", "layer": 1, "seed": 3}}
    mv = E.gen_game(11, 4, 1.0, 4)[0][:10].tolist()
    s = ns.acts_for_sequence(model, mv, "A", key)
    assert len(s) == len(mv) + 1
    p0 = ns.move_probs(model, mv)
    assert np.allclose(ns.move_probs(model, mv, "A", key, float(s[-1])), p0, atol=1e-5)  # setting to its own value is a no-op
    assert not np.allclose(ns.move_probs(model, mv, "B", key, 50.0), p0, atol=1e-3)
    moves = np.full((2, 42), -1, np.int8); moves[0, :10] = mv; moves[1, :6] = mv[:6]
    lengths = np.array([10, 6])
    S = ns.unit_acts(model, moves, lengths, ["A", "B"], key)
    assert np.allclose(S[:10, 0], s[:10], atol=1e-4)
    r = ns.kl_recovery(model, moves, lengths, "A", key, S[:, 0], S[:, 0])
    assert abs(r["recovery"] - 1) < 1e-4 or r["kl_zero"] < 1e-9


def test_eligible_mask():
    m = ns.eligible(np.array([3, 6]), 4)
    assert m.tolist() == [False] * 3 + [False] * 4 + [True] * 2
