def score(b):
    g = b.grid
    t0 = [0.0, 3.0, 1.0, -0.5, 2.0, 3.0, -2.0]
    m0 = [0.0, -2.0, 1.0, 2.5, -1.0, -1.0, 2.0]
    t1 = [0.0, -2.5, -0.5, -1.0, -2.5, -2.5, -2.5]
    m1 = [0.0, 0.5, 0.0, 1.3, -1.2, -1.2, 0.0]
    s = 0.0
    for c in range(7):
        v = g[0][c]
        if v == 2:
            s += t0[c]
        elif v == 1:
            s += m0[c]
        v = g[1][c]
        if v == 2:
            s += t1[c]
        elif v == 1:
            s += m1[c]
    return s

def fires(b):
    return score(b) >= 9.0

def level(b):
    s = score(b)
    if s < 7.5:
        return 0
    return max(0, min(9, int((s - 7.5) * 1.5)))
