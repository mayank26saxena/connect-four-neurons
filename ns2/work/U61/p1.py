def fires(b):
    g = b.grid
    return g[2][3] == 1 and g[1][3] == 2

def level(b):
    g = b.grid
    if not (g[2][3] == 1 and g[1][3] == 2):
        return 0
    s = 4
    if g[3][3] == 2:
        s += 2
    if g[1][2] == 1:
        s += 2
    if g[2][2] == 1:
        s += 1
    return min(s, 9)
