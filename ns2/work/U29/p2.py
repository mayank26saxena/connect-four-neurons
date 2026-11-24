def score(b):
    g = b.grid
    if g[4][4] != 0:
        return -5
    s = 0
    if g[4][3] == 2:
        s += 3
    if g[3][4] == 1:
        s -= 2
    if g[3][4] == 2:
        s += 1
    cues = [((2, 3), 1), ((3, 3), 1), ((1, 3), 2), ((1, 2), 2), ((2, 2), 1),
            ((1, 5), 1), ((5, 3), 1), ((2, 4), 1), ((0, 1), 2), ((0, 3), 1),
            ((2, 5), 2), ((3, 5), 2), ((0, 2), 1)]
    for (r, c), v in cues:
        if g[r][c] == v:
            s += 1
    return s

def fires(b):
    return score(b) >= 9

def level(b):
    s = score(b)
    return max(0, min(9, s - 3))
