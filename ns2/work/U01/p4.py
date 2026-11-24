# additive pattern over cells, (row, col, owner): owner 1 = me (X), 2 = them (O)
W = {
    (0, 0, 1): 3, (0, 6, 2): 1, (0, 3, 1): 1, (0, 3, 2): -2, (0, 1, 2): 1, (0, 1, 1): -1,
    (0, 4, 2): 1, (0, 4, 1): -1,
    (1, 4, 1): 2, (1, 4, 2): -1, (1, 1, 1): -2, (1, 6, 1): -1,
    (2, 4, 2): 3, (2, 4, 1): -2, (2, 2, 2): -3, (2, 5, 2): -2, (2, 3, 1): -2, (2, 6, 2): -1,
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

def gate(b):
    return b.grid[0][0] == 1 or (b.grid[2][4] == 2 and b.grid[1][4] == 1)

def fires(b):
    return gate(b) and points(b) >= 8

def level(b):
    if not gate(b):
        return 0
    return max(0, min(9, points(b) - 1))
