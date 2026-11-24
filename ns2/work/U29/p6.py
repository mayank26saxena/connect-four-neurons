def cues(b):
    g = b.grid
    s = 0
    if g[3][4] == 2:
        s += 1
    lst = [((2, 3), 1), ((3, 3), 1), ((1, 3), 2), ((1, 2), 2), ((2, 2), 1),
           ((1, 5), 1), ((5, 3), 1), ((2, 4), 1), ((0, 1), 2), ((0, 3), 1),
           ((2, 5), 2), ((3, 5), 2), ((0, 2), 1)]
    for (r, c), v in lst:
        if g[r][c] == v:
            s += 1
    return s

def core(b):
    g = b.grid
    return g[4][3] == 2 and g[5][3] != 2 and g[4][4] == 0 and g[3][4] != 1 and b.ply <= 28

def fires(b):
    return core(b) and cues(b) >= 5

def level(b):
    if not core(b):
        g = b.grid
        return 1 if (g[4][3] == 2 and g[4][4] == 0) else 0
    return max(2, min(9, cues(b) + 1))
