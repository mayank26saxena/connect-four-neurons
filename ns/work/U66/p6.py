def pts(b):
    h = b.heights
    g = b.grid
    s = 0.0
    lc = b.last_col
    s += {0: 1.5, 6: 2.0, 2: 1.0, 4: 0.3}.get(lc, -1.0)
    s += {1: 1.0, 2: 1.5, 3: 0.3, 4: 0.6}.get(h[4], -1.5)
    for c in (1, 3, 5):
        if h[c] == 0: s += 0.6
    if g[0][0] == 2: s += 0.5
    if g[0][4] == 2: s += 0.5
    if h[6] >= 3 and g[h[6] - 1][6] == 2 and g[h[6] - 2][6] == 2: s += 1.0
    if len(b.moves) >= 2 and b.moves[-2] in (3, 4): s += 0.5
    return s

def fires(b):
    return pts(b) >= 4.8

def level(b):
    return max(0, min(9, int(round((pts(b) - 2.0) * 1.6))))
