def pts(b):
    h = b.heights
    g = b.grid
    s = {0: -3, 1: 1, 2: 2, 3: 0.5, 4: 0.5}.get(h[4], -3)
    if h[1] == 0: s += 1
    if h[5] == 0: s += 1
    if h[6] in (3, 4): s += 1
    if g[1][6] == 2 and g[2][6] == 2: s += 1.5
    if g[0][0] == 2: s += 1
    if g[0][4] == 2: s += 0.5
    if g[1][4] == 1: s += 0.5
    if b.last_col == 6: s += 1
    return s

def fires(b):
    return pts(b) >= 6

def level(b):
    return max(0, min(9, int(round((pts(b) - 3) * 1.5))))
