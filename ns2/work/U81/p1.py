def fires(b):
    g = b.grid
    if g[0][2] != 1:
        return False
    if b.heights[6] > 1 or b.ply > 24:
        return False
    return g[0][3] == 2 or g[0][6] == 2

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    s = 3
    if g[0][3] == 2 and g[0][6] == 2:
        s += 3
    if g[0][4] == 1:
        s += 2
    return min(s, 9)
