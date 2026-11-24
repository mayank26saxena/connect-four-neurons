def score_(b):
    if b.heights[5] != 1:
        return -9
    g = b.grid
    s = 0
    if g[0][5] == 2:
        s += 2
    if g[0][6] == 1:
        s += 2
    elif g[0][6] == 2:
        s -= 1
    if g[0][4] == 1:
        s += 1
    elif g[0][4] == 0:
        s -= 4
    if g[0][3] == 0:
        s -= 2
    if g[1][4] == 2:
        s += 1
    elif g[1][4] == 1:
        s -= 1
    if g[1][3] == 2:
        s += 1
    elif g[1][3] == 1:
        s -= 3
    if g[0][2] == 2:
        s += 1
    if b.ply < 12:
        s += 1
    elif b.ply > 24:
        s -= 1
    return s

def fires(b):
    return score_(b) >= 5

def level(b):
    s = score_(b)
    if s < 2:
        return 0
    return min(9, (s - 2) * 2)
