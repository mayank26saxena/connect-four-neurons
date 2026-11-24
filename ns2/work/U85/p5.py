def points(b):
    g = b.grid
    h = b.heights
    s = 0.0
    if h[3] == 3:
        s += 3
    elif h[3] == 4:
        s += 1.5
    elif h[3] in (2, 5):
        s += 0.5
    if g[3][2] == 2:
        s += 2
    elif g[3][2] == 1:
        s += 0.5
    if h[2] >= 4:
        s += 1
    elif h[2] == 3:
        s += 0.5
    if h[1] >= 4:
        s += 0.5
    if g[1][3] == 1:
        s += 1
    if g[0][3] == 2:
        s += 0.5
    if g[2][1] == 2:
        s += 0.5
    if g[3][1] == 2:
        s += 0.5
    if g[4][2] == 2:
        s += 0.5
    if g[4][4] == 2:
        s += 0.5
    return s

def fires(b):
    return points(b) >= 6

def level(b):
    p = points(b)
    return max(0, min(9, int(p * 1.2) - 2))
