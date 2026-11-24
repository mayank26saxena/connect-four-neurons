def fires(b):
    g = b.grid
    return g[0][1] == 2 and g[0][2] == 1 and g[0][0] != 2

def level(b):
    return 6 if fires(b) else 0
