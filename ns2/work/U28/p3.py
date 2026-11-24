def fires(b):
    g = b.grid
    return g[0][2] == 2 and g[0][3] != 2 and b.ply <= 20 and b.heights[1] <= 2 and b.heights[4] <= 2


def level(b):
    return 6 if fires(b) else 0
