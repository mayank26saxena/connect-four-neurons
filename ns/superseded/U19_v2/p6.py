# weights: (cell): (weight if theirs, weight if mine); applies only while (1,4) is empty
W = {
    (1, 5): (3.0, -1.5),
    (1, 3): (1.5, -1.0),
    (0, 3): (1.0, -2.5),
    (1, 2): (1.0, 0.0),
    (0, 2): (0.7, 0.0),
    (0, 5): (0.0, 1.0),
    (0, 4): (0.0, 1.5),
    (2, 5): (-2.0, -2.0),
    (0, 6): (-2.0, -1.5),
    (1, 6): (-1.0, 0.0),
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

def early(b):
    return score(b) >= 4.0

def late(b):
    if b.ply < 18 or b.grid[1][5] != 2:
        return False
    n = sum(1 for c in range(1, 6) if b.grid[1][c] == 2)
    return n >= 3

def fires(b):
    return early(b) or late(b)

def level(b):
    s = score(b)
    if late(b):
        s = max(s, 4.5)
    if s < 3.0:
        return 0
    return max(1, min(9, int(round((s - 3.0) * 2))))
