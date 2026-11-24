def score_(b):
    h = b.heights
    g = b.grid
    if h[1] == 0 or h[2] == 0:
        return 0
    if h[0] == 0:
        s = 0
    elif h[0] >= 4 and g[0][0] == 1 and g[1][0] == 2 and g[2][0] == 1 and g[3][0] == 2:
        s = 1
    else:
        return 0
    if g[0][1] == 2:
        s += 2
    if g[0][2] == 1:
        s += 1
    if h[3] > 0:
        s += 1
    if h[4] == 0:
        s += 2
    if b.ply <= 12:
        s += 2
    return s

def fires(b):
    return score_(b) >= 6

def level(b):
    s = score_(b)
    return max(0, min(9, (s - 3) * 2))
