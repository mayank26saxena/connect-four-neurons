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
    o = sum(1 for (r, c) in [(1, 2), (1, 3), (2, 2)] if g[r][c] == 2)
    s += min(o, 2)
    if g[1][1] == 2 or g[1][4] == 2 or g[0][0] == 2:
        s -= 2
    return max(0, s)

def fires(b):
    return _s(b) >= 6

def level(b):
    return [0, 0, 0, 0, 0, 1, 4, 8][_s(b)]
