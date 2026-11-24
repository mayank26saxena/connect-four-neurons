def fires(b):
    g = b.grid
    if b.ply > 14:
        return False
    if any(g[r][6] == 1 for r in range(6)):
        return False
    if g[0][2] == 1:
        return False
    return g[1][3] == 2 or g[1][5] == 2

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    s = 3 + 2 * (g[1][3] == 2) + 2 * (g[1][5] == 2) + (g[2][3] == 1)
    return min(9, s)
