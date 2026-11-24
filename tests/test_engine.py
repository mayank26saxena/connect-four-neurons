import numpy as np

from c4n import engine as E
from c4n.concepts import INDEX, game_concepts


def brute_board(moves):
    g = np.zeros((6, 7), dtype=int)  # 1 first player, 2 second
    h = [0] * 7
    for i, c in enumerate(moves):
        g[h[c], c] = 1 + i % 2
        h[c] += 1
    return g, h


def four(g, p):
    for r in range(6):
        for c in range(7):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(0 <= r + k * dr < 6 and 0 <= c + k * dc < 7 and g[r + k * dr, c + k * dc] == p for k in range(4)):
                    return True
    return False


def brute_threats(g, p):
    out = np.zeros((6, 7), dtype=bool)
    for r in range(6):
        for c in range(7):
            if g[r, c] == 0:
                g2 = g.copy(); g2[r, c] = p
                out[r, c] = four(g2, p)
    return out


def random_games(n, seed=0):
    rng = np.random.default_rng(seed)
    games = []
    for _ in range(n):
        g, h, mv = np.zeros((6, 7), int), [0] * 7, []
        for i in range(42):
            legal = [c for c in range(7) if h[c] < 6]
            c = int(rng.choice(legal))
            g[h[c], c] = 1 + i % 2; h[c] += 1; mv.append(c)
            if four(g, 1 + i % 2):
                break
        games.append(np.array(mv, dtype=np.int8))
    return games


def test_threat_cells_match_brute_force():
    for mv in random_games(60):
        pos, mask = E.replay_boards(mv)
        for t in range(len(mv)):
            g, _ = brute_board(mv[:t])
            me = 1 + t % 2
            got_me = E.bits_to_grid(E.winning_cells(pos[t:t + 1], mask[t:t + 1]))[0]
            got_op = E.bits_to_grid(E.winning_cells(pos[t:t + 1] ^ mask[t:t + 1], mask[t:t + 1]))[0]
            assert (got_me == brute_threats(g, me)).all()
            assert (got_op == brute_threats(g, 3 - me)).all()


def test_teacher_takes_win_and_blocks():
    # first player has three in the bottom row at columns 0-2; first player to move -> win at 3
    s = E.score_moves([0, 6, 1, 6, 2, 5], depth=4)
    assert s.argmax() == 3 and s[3] >= E.WIN_SCORE - 42
    # second player to move must block column 3
    s = E.score_moves([0, 6, 1, 6, 2], depth=4)
    assert s.argmax() == 3


def test_gen_game_deterministic():
    a = E.gen_game(123, 4, 2.0, 2)
    E.gen_game(999, 6, 1.0, 0)  # pollute transposition table
    b = E.gen_game(123, 4, 2.0, 2)
    assert (a[0] == b[0]).all() and (a[1] == b[1]).all() and a[2] == b[2]


def test_concepts_consistent():
    for seed in range(20):
        mv, sc, _ = E.gen_game(seed, 4, 2.0, 4)
        X = game_concepts(mv, sc)
        for t in range(len(mv)):
            g, h = brute_board(mv[:t])
            me = 1 + t % 2
            thr_op = brute_threats(g, 3 - me)
            for c in range(7):
                blk = h[c] < 6 and thr_op[h[c], c]
                assert X[t, INDEX[f"block_now_c{c}"]] == blk
                assert X[t, INDEX[f"full_c{c}"]] == (h[c] == 6)
            assert X[t, INDEX["cell_r0c0_mine"]] == (g[0, 0] == me)


def test_line_concepts_match_brute_force():
    from c4n.concepts import WINDOWS
    assert len(WINDOWS) == 69
    for seed in range(10):
        mv, sc, _ = E.gen_game(seed, 4, 2.0, 4)
        X = game_concepts(mv, sc)
        for t in range(len(mv)):
            g, _ = brute_board(mv[:t])
            me = 1 + t % 2
            for w, cells in WINDOWS:
                vals = [g[r, c] for r, c in cells]
                m, o = vals.count(me), vals.count(3 - me)
                for k in (2, 3):
                    assert X[t, INDEX[f"line_{w}_mine{k}"]] == (m == k and o == 0)
                    assert X[t, INDEX[f"line_{w}_theirs{k}"]] == (o == k and m == 0)
