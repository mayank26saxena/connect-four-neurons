import numpy as np

from c4n import engine as E
from c4n import tactics as T


def play_drop(g, h, c, p):
    g = g.copy(); h = list(h); g[h[c], c] = p; h[c] += 1
    return g, h


def four(g, p):
    for r in range(6):
        for c in range(7):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(0 <= r + k * dr < 6 and 0 <= c + k * dc < 7 and g[r + k * dr, c + k * dc] == p for k in range(4)):
                    return True
    return False


def immediate_wins(g, h, p):
    return [c for c in range(7) if h[c] < 6 and four(play_drop(g, h, c, p)[0], p)]


def brute(moves):
    """win, block, poison, fork column sets for the position after `moves` (player to move = 1 + len % 2)."""
    g, h = np.zeros((6, 7), int), [0] * 7
    for i, c in enumerate(moves):
        g, h = play_drop(g, h, c, 1 + i % 2)
    me, op = 1 + len(moves) % 2, 2 - len(moves) % 2
    win, block = immediate_wins(g, h, me), immediate_wins(g, h, op)
    poison, fork = [], []
    for c in range(7):
        if h[c] >= 6:
            continue
        g2, h2 = play_drop(g, h, c, me)
        if h2[c] < 6 and four(play_drop(g2, h2, c, op)[0], op) and not four(g2, me):
            poison.append(c)
        if not win and not block and not four(g2, me) and len(immediate_wins(g2, h2, me)) >= 2 and not immediate_wins(g2, h2, op):
            fork.append(c)
    return set(win), set(block), set(poison), set(fork)


def test_tactic_masks_match_brute_force():
    n_fork = 0
    for seed in range(60):
        mv, _, _ = E.gen_game(seed, 2, 4.0, 6)
        mv = mv[:-1] if len(mv) > 8 else mv
        lengths = np.array([len(mv)])
        pos, mask = T.boards(np.array([mv]), lengths)
        m = T.tactic_masks(pos, mask)
        for t in range(len(mv)):
            w, b, p, f = brute(list(mv[:t]))
            assert set(np.flatnonzero(m["win"][t])) == w
            assert set(np.flatnonzero(m["block"][t])) == b
            assert set(np.flatnonzero(m["poison"][t])) == p, (seed, t)
            assert set(np.flatnonzero(m["fork"][t])) == f, (seed, t)
            n_fork += bool(f)
    assert n_fork > 0, "test positions never contained a fork"
