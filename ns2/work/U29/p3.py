def core(b):
    g = b.grid
    return g[4][3] == 2 and g[5][3] != 2 and g[4][4] == 0 and g[3][4] != 1 and b.ply <= 28

def fires(b):
    return core(b)

def level(b):
    g = b.grid
    if core(b):
        s = 6
        if g[5][3] == 1:
            s += 1
        if g[3][4] == 2:
            s += 1
        if b.heights[4] <= 1:
            s += 1
        return s
    h = b.heights[3]
    if h in (2, 4) and g[h - 1][3] == 2 and b.heights[4] < h:
        return 3
    if g[4][3] == 2 and g[4][4] == 0:
        return 2
    return 0
