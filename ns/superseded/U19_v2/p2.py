W = {
    (1, 5): (3.0, -1.5),
    (2, 5): (-1.0, -1.0),
    (0, 5): (-0.5, 1.0),
    (0, 4): (0.0, 0.5),
    (0, 6): (0.0, -0.5),
    (0, 2): (1.0, 0.0),
    (0, 3): (1.0, 0.0),
    (1, 3): (1.0, 0.0),
    (1, 2): (1.0, -1.0),
    (1, 4): (-1.0, 0.0),
}

def score(b):
    s = 0.0
    for (r, c), (wo, wx) in W.items():
        v = b.grid[r][c]
        if v == 2:
            s += wo
        elif v == 1:
            s += wx
    return s

def fires(b):
    return score(b) >= 4.0

def level(b):
    s = score(b)
    if s < 2.0:
        return 0
    return max(0, min(9, int(round((s - 2.0) * 1.5))))
