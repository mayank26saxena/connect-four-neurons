def fires(b):
    g = b.grid
    if g[3][3] != 2 or g[3][2] != 0 or g[3][5] == 2:
        return False
    return g[2][4] == 2 or g[2][3] == 2

def level(b):
    g = b.grid
    if not fires(b):
        return 0
    n = (g[2][4] == 2) + (g[2][3] == 2) + (g[1][5] == 2) + (g[3][1] == 1)
    return 3 + 2 * n
