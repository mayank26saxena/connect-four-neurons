def late(b):
    g = b.grid
    return b.heights[2] >= 5 and g[4][2] == 2 and g[3][1] != 1 and b.heights[3] % 2 == 0

def fires(b):
    return late(b)

def level(b):
    if not late(b):
        return 0
    g = b.grid
    s = 4
    if g[3][1] == 2:
        s += 2
    if g[2][0] == 2:
        s += 1
    if b.heights[2] == 5:
        s += 1
    return min(9, s)
