def fires(b):
    g = b.grid
    if not (g[0][4] == 2 and g[1][4] == 2):
        return False
    if g[1][5] == 2:
        return False
    return b.ply <= 20

def level(b):
    g = b.grid
    if fires(b):
        s = 5
        if b.heights[1] <= 1:
            s += 1
        if b.heights[2] <= 1 or b.heights[3] <= 1:
            s += 1
        return s
    if g[0][4] == 2 and g[1][4] == 2:
        return 2
    return 0
