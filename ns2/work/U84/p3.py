def _s(b):
    h = b.heights
    g = b.grid
    s = 0
    if h[0] <= 1:
        s += 2
    elif h[0] == 2:
        s += 1
    else:
        return 0
    if h[1] in (2, 3):
        s += 2
    elif h[1] in (1, 4):
        s += 1
    if h[3] not in (3, 4):
        s += 1
    if h[4] not in (2, 3):
        s += 1
    if g[1][1] == 1:
        s += 1
    if g[2][2] == 1:
        s += 1
    if g[1][2] == 2:
        s += 1
    return s

def fires(b):
    return _s(b) >= 8

def level(b):
    return min(9, _s(b))
