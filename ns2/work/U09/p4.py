def score(b):
    g = b.grid
    t0 = [0.0, 3.0, 1.0, -0.5, 2.0, 3.0, -2.0]
    m0 = [0.0, -2.0, 1.0, 2.5, -1.0, -1.0, 2.0]
    s = 0.0
    for c in range(7):
        v = g[0][c]
        if v == 2:
            s += t0[c]
        elif v == 1:
            s += m0[c]
    for c in (1, 4, 5, 6):
        if g[1][c] == 2:
            s -= 2.5
    if g[1][3] == 1:
        s += 1.0
    s -= 0.25 * max(0, b.ply - 7)
    return s

def fires(b):
    return score(b) >= 8.0

def level(b):
    s = score(b)
    if s < 6.5:
        return 0
    return max(0, min(9, int((s - 6.5) * 1.5)))
