def fires(b):
    g = b.grid
    if not (g[0][4] == 2 and g[1][4] == 2):
        return False
    if g[1][5] == 2:
        return False
    if g[0][3] == 1 and g[1][3] == 1:
        return False
    return b.ply <= 22

def level(b):
    g = b.grid
    if fires(b):
        return 7
    if g[0][4] == 2 and g[1][4] == 2:
        return 3
    return 0
