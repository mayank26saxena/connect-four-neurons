GOOD_THEM = [(1, 3), (0, 6), (0, 1), (2, 1), (2, 5)]
BAD_THEM = [(1, 2), (2, 2), (1, 4), (2, 4), (1, 5)]
GOOD_ME = [(1, 1), (1, 5)]
BAD_ME = [(0, 2), (0, 1)]

def score(b):
    g = b.grid
    s = 0
    s += sum(1 for (r, c) in GOOD_THEM if g[r][c] == 2)
    s -= sum(1 for (r, c) in BAD_THEM if g[r][c] == 2)
    s += sum(1 for (r, c) in GOOD_ME if g[r][c] == 1)
    s -= sum(1 for (r, c) in BAD_ME if g[r][c] == 1)
    if b.heights[3] == 6:
        s -= 1
    if b.ply > 24:
        s -= 1
    return s

def fires(b):
    return score(b) >= 3

def level(b):
    return max(0, min(9, 2 * score(b) + 2))
