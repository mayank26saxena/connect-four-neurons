# weights: (cell): (weight if theirs, weight if mine)
W = {
    (1, 5): (3.0, -1.5),
    (1, 3): (1.5, -1.0),
    (0, 3): (1.0, -2.5),
    (1, 2): (1.0, 0.0),
    (0, 2): (0.7, 0.0),
    (0, 5): (0.0, 1.0),
    (0, 4): (0.0, 0.5),
    (2, 5): (-2.0, -2.0),
    (0, 6): (0.0, -1.0),
}

def score(b):
    if b.grid[1][4] != 0:
        return 0.0
    s = 0.0
    for (r, c), (wo, wx) in W.items():
        v = b.grid[r][c]
        if v == 2:
            s += wo
        elif v == 1:
            s += wx
    return s

def fires(b):
    return score(b) >= 3.5

def level(b):
    s = score(b)
    return max(0, min(9, int(round((s - 2.0) * 1.5))))
