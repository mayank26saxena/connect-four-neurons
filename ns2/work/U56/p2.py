def fires(b):
    g = b.grid
    return g[0][0] == 0 and g[0][1] == 2 and g[0][2] != 0

def level(b):
    g = b.grid
    if not fires(b):
        return 0
    s = 4
    if g[0][2] == 1:
        s += 2
    if g[0][3] != 0:
        s += 1
    if g[0][4] != 0:
        s -= 2
    return s
