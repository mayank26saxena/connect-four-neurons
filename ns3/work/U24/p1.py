def fires(b):
    g = b.grid
    return g[0][3] == 1 and g[1][3] == 1 and g[2][3] == 2

def level(b):
    g = b.grid
    s = (g[0][3] == 1) + (g[1][3] == 1) + (g[2][3] == 2)
    return [0, 1, 3, 7][s]
