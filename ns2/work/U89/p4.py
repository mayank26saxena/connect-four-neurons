W = {
    (0, 4, 2): 1.5, (0, 4, 1): -1.0,
    (0, 5, 1): 1.2, (0, 5, 2): -0.8,
    (0, 0, 2): 1.0,
    (0, 3, 2): 0.5,
    (1, 3, 2): 1.0, (1, 3, 1): -1.2,
    (1, 2, 1): 1.2, (1, 2, 2): -1.2,
    (2, 2, 2): 2.0, (2, 2, 1): -1.5,
    (3, 2, 1): 1.0,
    (1, 4, 2): 0.5, (1, 4, 1): -0.6,
    (2, 4, 2): -2.0,
    (1, 5, 2): -0.8,
}

def score(b):
    g = b.grid
    s = 0.0
    for r in range(4):
        for c in range(7):
            v = g[r][c]
            if v:
                s += W.get((r, c, v), 0.0)
    s -= 1.0 * b.heights[1]
    s -= 0.08 * b.ply
    if b.their_playable_wins:
        s -= 2.0
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 1.5:
        return 0
    return max(0, min(9, int((s - 1.5) * 1.5)))
