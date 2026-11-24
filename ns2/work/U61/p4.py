def alt3(b):
    g = b.grid
    h = b.heights[3]
    if h < 3 or h > 5:
        return False
    for r in range(1, h):
        if g[r][3] == g[r - 1][3]:
            return False
    return g[2][3] == 1

def fires(b):
    g = b.grid
    if not alt3(b):
        return False
    return b.heights[4] <= 2 and g[2][2] != 2 and g[2][4] != 2

def level(b):
    g = b.grid
    if not alt3(b):
        return 1 if g[2][3] == 1 else 0
    s = 4
    if b.heights[4] <= 2:
        s += 2
    if g[1][2] == 1:
        s += 1
    if g[2][2] == 1:
        s += 1
    if g[2][2] == 2 or g[2][4] == 2:
        s -= 3
    return max(0, min(9, s))
