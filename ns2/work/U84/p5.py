def _s(b):
    g = b.grid
    h = b.heights
    if h[0] > 2:
        return 0
    s = 2 if h[0] <= 1 else 0
    s += (g[1][1] == 1) + (g[2][1] == 2) + (g[1][2] == 2) + (g[2][2] == 1)
    s += (g[0][2] == 2) + (g[0][4] == 1) + (g[0][1] == 2 and g[1][1] == 0)
    if h[3] in (3, 4):
        s -= 1
    if g[0][0] == 1:
        s -= 1
    return s

def fires(b):
    return _s(b) >= 6

def level(b):
    return max(0, min(9, _s(b)))
