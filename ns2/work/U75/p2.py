def fires(b):
    g = b.grid
    return g[2][2] == 0 and g[1][2] != 1 and g[1][3] != 2 and g[0][1] == 1

def level(b):
    return 6 if fires(b) else 0
