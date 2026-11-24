# hand-set cell weights read off single-cell occupancy histograms (firing bands vs low bands)
W = {
    (3, 3): (3.0, -4.0),
    (2, 4): (1.5, -2.0),
    (3, 5): (-2.0, 0.7),
    (3, 1): (-1.0, 0.7),
    (3, 2): (-1.0, -1.0),
    (4, 3): (-0.3, 0.8),
    (1, 4): (0.0, 0.8),
    (1, 5): (0.7, 0.0),
    (3, 0): (0.7, 0.0),
    (2, 0): (0.0, 0.5),
    (5, 3): (0.0, 0.8),
    (0, 6): (0.0, 0.6),
    (2, 3): (0.5, 0.5),
}

def score(b):
    s = 0.0
    for (r, c), (wt, wm) in W.items():
        v = b.grid[r][c]
        if v == 2:
            s += wt
        elif v == 1:
            s += wm
    return s

def fires(b):
    return score(b) >= 6.0

def level(b):
    s = score(b)
    return max(0, min(9, int(round(s - 2))))
