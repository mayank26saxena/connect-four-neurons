def pts(b):
    g = b.grid
    h = b.heights
    s = 0
    if g[0][6] == 1:
        s += 1
    if g[1][6] == 2:
        s += 1
    if h[6] in (2, 3):
        s += 1
    if g[2][5] == 2:
        s += 1
    if h[5] in (2, 3, 4):
        s += 1
    if h[2] in (0, 6):
        s += 1
    return s

def fires(b):
    return pts(b) >= 5

def level(b):
    return pts(b)
