def fires(b):
    g = b.grid
    return g[3][3] == 2 and g[2][4] == 2 and g[3][5] != 2 and g[3][2] == 0

def level(b):
    return 6 if fires(b) else 0
