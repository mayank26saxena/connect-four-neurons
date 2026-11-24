def fires(b):
    g = b.grid
    if b.ply > 16:
        return False
    if b.ply == 1:
        return g[0][1] == 2
    bottom = g[0][1] == 2 and g[0][5] == 2 and g[0][0] != 2 and g[0][6] != 2
    tower = b.heights[3] >= 4 and g[0][3] == 2 and g[1][3] == 2 and g[2][3] == 1 and g[3][3] == 2
    return bottom or tower

def level(b):
    if not fires(b):
        return 0
    s = 5
    if b.grid[0][2] == 1:
        s += 2
    if b.ply <= 10:
        s += 2
    return s
