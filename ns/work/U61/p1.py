def fires(b):
    g = b.grid
    bottom = g[0][1] == 2 and g[0][5] == 2 and g[0][0] != 2 and g[0][6] != 2
    tower = b.heights[3] >= 4 and g[0][3] == 2 and g[1][3] == 2 and g[2][3] == 1 and g[3][3] == 2
    return bottom or tower

def level(b):
    return 7 if fires(b) else 0
