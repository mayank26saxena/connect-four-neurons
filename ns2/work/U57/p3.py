def fires(b):
    g = b.grid
    if g[0][4] != 2:
        return False
    if g[1][5] == 2:
        return False
    return b.heights[4] <= 4 and b.ply <= 24

def level(b):
    g = b.grid
    if not fires(b):
        return 1 if g[0][4] == 2 else 0
    s = 4
    if g[1][4] == 2:
        s += 2
    if b.heights[1] == 0 or g[0][1] == 1:
        s += 1
    return min(s, 9)
