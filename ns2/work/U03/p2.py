def score_(b):
    if b.heights[5] != 1:
        return -1
    g = b.grid
    s = 0
    if g[0][5] == 2:
        s += 2
    if g[0][6] == 1:
        s += 2
    if g[0][4] == 1:
        s += 1
    if g[0][3] != 0:
        s += 1
    if g[0][4] == 0:
        s -= 3
    if g[1][4] == 2:
        s += 1
    if g[1][3] == 2:
        s += 1
    if g[0][2] == 2:
        s += 1
    return s

def fires(b):
    return score_(b) >= 6

def level(b):
    s = score_(b)
    if s < 3:
        return 0
    return min(9, (s - 3) * 2)
