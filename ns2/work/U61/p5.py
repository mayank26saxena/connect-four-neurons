def fires(b):
    g = b.grid
    if g[2][3] != 1:
        return False
    if g[2][4] != 0 or g[3][4] != 0:
        return False
    if g[2][2] == 2 or g[0][1] == 2 or g[0][2] == 2:
        return False
    return b.heights[3] >= 3

def level(b):
    g = b.grid
    if not fires(b):
        return 1 if g[2][3] == 1 else 0
    s = 5
    if g[1][3] == 2:
        s += 1
    if g[3][3] == 2:
        s += 1
    if g[1][2] == 1:
        s += 2
    return min(9, s)
