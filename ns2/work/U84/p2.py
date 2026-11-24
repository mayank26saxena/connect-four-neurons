def _s(b):
    g = b.grid
    if b.heights[0] > 1:
        return 0
    if not (g[1][1] == 1 and g[1][2] == 2):
        return 0
    s = 0
    if g[2][2] == 1:
        s += 3
    if g[2][1] == 2:
        s += 2
    if g[0][3] == 2:
        s += 2
    if g[0][4] == 1:
        s += 1
    if b.heights[0] == 0:
        s += 1
    return s

def fires(b):
    return _s(b) >= 4

def level(b):
    return min(9, _s(b))
