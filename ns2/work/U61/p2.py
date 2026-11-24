def fires(b):
    g = b.grid
    return g[2][3] == 1 and b.heights[4] <= 2 and g[2][2] != 2

def level(b):
    g = b.grid
    if not fires(b):
        return 0
    s = 3
    if g[1][3] == 2:
        s += 2
    if g[3][3] == 2:
        s += 1
    if g[1][2] == 1:
        s += 2
    if g[0][3] == 1:
        s += 1
    return min(s, 9)
