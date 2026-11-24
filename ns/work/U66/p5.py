def pts(b):
    h = b.heights
    g = b.grid
    s = 0.0
    lc = b.last_col
    s += {0: 1.5, 6: 2.0, 2: 1.0, 4: 0.3}.get(lc, -1.0)
    s += {1: 1.0, 2: 1.5, 3: 0.3, 4: 0.6}.get(h[4], -1.5)
    if h[1] == 0: s += 0.5
    if h[5] == 0: s += 0.5
    if g[0][0] == 2: s += 0.5
    if g[0][4] == 2: s += 0.5
    if h[6] >= 3 and g[h[6] - 1][6] == 2 and g[h[6] - 2][6] == 2: s += 1.0
    return s

def fires(b):
    return pts(b) >= 4.5

def level(b):
    return max(0, min(9, int(round((pts(b) - 2.0) * 1.8))))
