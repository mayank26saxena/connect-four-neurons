def fires(b):
    g = b.grid
    return g[1][3] == 2 and g[2][3] != 2 and g[2][4] == 0 and g[1][4] != 1

def level(b):
    g = b.grid
    if not fires(b):
        return 0
    s = 3
    if g[2][3] == 1:
        s += 3
    if g[0][2] != 0:
        s += 2
    if g[1][4] == 0:
        s += 1
    return min(s, 9)
