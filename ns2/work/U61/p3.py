def score_(b):
    g = b.grid
    s = 0
    if g[2][3] == 1:
        s += 3
    if g[1][3] == 2:
        s += 2
    if g[3][3] == 2:
        s += 1
    if g[0][3] == 1:
        s += 1
    if g[1][2] == 1:
        s += 1
    if g[2][2] == 1:
        s += 1
    if g[3][2] == 2:
        s += 1
    if g[2][4] == 2 or g[3][4] == 2:
        s -= 3
    if b.heights[4] >= 3:
        s -= 1
    if g[2][2] == 2:
        s -= 2
    return s

def fires(b):
    return score_(b) >= 8

def level(b):
    s = score_(b)
    return max(0, min(9, s - 1))
