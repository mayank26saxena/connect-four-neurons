def fires(b):
    g = b.grid
    if b.heights[2] > 1:
        return False
    return g[2][1] == 1 and g[0][1] == 2

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    s = 4
    if g[1][1] == 1:
        s += 2
    if g[3][1] == 2:
        s += 2
    if b.heights[2] == 0:
        s += 1
    return s
