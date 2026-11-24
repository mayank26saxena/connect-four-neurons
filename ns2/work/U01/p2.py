# additive pattern: weights for (row, col, owner) with owner 1 = me (X), 2 = them (O)
W = {
    (0, 0, 1): 2, (0, 6, 2): 2, (0, 3, 1): 1, (0, 1, 2): 1, (0, 4, 2): 1,
    (1, 4, 1): 2, (1, 1, 2): 1, (1, 1, 1): -2, (1, 6, 1): -1,
    (2, 4, 2): 3, (2, 2, 2): -3, (2, 5, 2): -2, (2, 3, 1): -2,
    (3, 4, 1): 2, (3, 3, 2): -2, (3, 1, 2): 1,
    (4, 4, 1): 1, (4, 3, 1): -2,
    (5, 5, 2): 1,
}

def points(b):
    s = 0
    for (r, c, p), w in W.items():
        if b.grid[r][c] == p:
            s += w
    return s

def fires(b):
    return points(b) >= 8

def level(b):
    return max(0, min(9, points(b) - 2))
