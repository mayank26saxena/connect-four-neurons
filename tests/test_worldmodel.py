import numpy as np
import torch

from c4n import engine as E
from c4n import worldmodel as WM




def test_score_board_matches_score_moves():
    for seed in range(5):
        mv = E.gen_game(seed, 4, 1.0, 4)[0][:12]
        p, m = E.replay_boards(mv)
        assert (E.score_board(p[-1], m[-1], 6) == E.score_moves(mv, 6)).all()


def test_labels():
    mv = E.gen_game(3, 4, 1.0, 4)[0]
    moves = np.full((1, 42), -1, np.int8); moves[0, : len(mv)] = mv
    lab = WM.board_labels(moves, np.array([len(mv)]))
    for t in range(len(mv)):
        rel, ab = lab["rel"][t], lab["abs"][t]
        assert (ab == 1).sum() == (t + 1) // 2 and (ab == 2).sum() == t // 2  # first player has moved ceil(t/2) times
        assert ((rel == 0) == (ab == 0)).all()
        # the player to move has made t // 2 moves
        assert (rel == WM.MINE).sum() == t // 2


def test_edit_alpha_hits_margin():
    torch.manual_seed(0)
    B, d = 64, 16
    x, W, b = torch.randn(B, d), torch.randn(B, d, 3), torch.randn(B, 3)
    src, tgt = torch.zeros(B, dtype=torch.long), torch.ones(B, dtype=torch.long) * 2
    m = torch.full((B,), 3.0)
    a, u = WM.edit_alpha(x, W, b, src, tgt, m)
    lg = torch.einsum("bd,bdc->bc", x + a[:, None] * u, W) + b
    mg = lg[:, 2] - torch.maximum(lg[:, 0], lg[:, 1])
    ok = a > 0
    assert torch.allclose(mg[ok], m[ok], atol=1e-3) or (mg[ok] >= m[ok] - 1e-3).all()


def test_candidate_edits_keep_gravity():
    mv = E.gen_game(5, 4, 1.0, 4)[0][:15]
    p, m = E.replay_boards(mv)
    for kind, k, src, tgt, np_, nm in WM.candidate_edits(int(p[-1]), int(m[-1])):
        nm = np.uint64(nm)
        assert (np.uint64(np_) & ~nm) == 0
        g = E.bits_to_grid(np.array([nm]))[0]
        for c in range(7):  # no floating stones
            col = g[:, c]
            assert not any(col[r] and not col[r - 1] for r in range(1, 6))
