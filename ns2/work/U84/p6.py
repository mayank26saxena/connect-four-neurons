def _s(b):
    h = b.heights
    g = b.grid
    if h[0] > 2:
        return 0
    s = 2 if h[0] <= 1 else 0
    if h[0] == 0:
        s += 1
    if h[1] in (2, 3):
        s += 2
    elif h[1] in (1, 4):
        s += 1
    if h[3] not in (3, 4):
        s += 1
    if h[4] not in (2, 3):
        s += 1
    if h[6] <= 1:
        s += 1
    s += (g[1][1] == 1) + (g[2][2] == 1) + (g[1][2] == 2) + (g[2][1] == 2)
    return s

def fires(b):
    return _s(b) >= 9

def level(b):
    return max(0, min(9, _s(b) - 4))
