def fires(b):
    g = b.grid
    if g[4][4] != 0 or g[3][4] == 1 or b.ply > 28:
        return False
    return g[4][3] == 2 or (g[3][4] == 2 and b.heights[3] >= 4)

def level(b):
    g = b.grid
    if not fires(b):
        return 1 if (g[4][3] == 2 and g[4][4] == 0) else 0
    s = 5
    if g[4][3] == 2 and g[3][4] == 2:
        s += 2
    if g[4][3] == 2 and g[5][3] != 2:
        s += 1
    if b.last_col == 4 or b.last_row == 3:
        s += 1
    return min(9, s)
