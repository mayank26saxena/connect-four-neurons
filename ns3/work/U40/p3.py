def _s(b):
    h = b.heights
    g = b.grid
    if b.ply > 14:
        return 0
    s = 0
    if h[3] >= 2: s += 1
    if h[2] >= 1: s += 1
    if h[4] <= 1: s += 1
    if h[1] <= 1: s += 1
    if h[0] == 0: s += 1
    o = sum(1 for (r, c) in [(1, 2), (1, 3), (2, 2), (2, 3)] if g[r][c] == 2)
    if o >= 1: s += 1
    if o >= 2: s += 1
    return s

def fires(b):
    return _s(b) >= 6

def level(b):
    s = _s(b)
    return [0, 0, 0, 0, 1, 2, 4, 7][s]
