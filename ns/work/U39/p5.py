def score(b):
    h = b.heights
    g = b.grid
    s = 0
    if 4 <= h[3] <= 5:
        s += 2
    elif h[3] in (1, 2):
        s -= 2
    elif h[3] == 3:
        s -= 1
    elif h[3] == 6:
        s -= 3
    if h[2] >= 3:
        s += 1
    if h[2] == 6:
        s -= 2
    if h[3] == 0 and h[2] >= 3:
        s += 1
    if h[0] >= 2:
        s += 1
    s -= max(0, h[4] - 1)
    s -= max(0, h[5] - 2)
    s -= max(0, h[6] - 2)
    s -= max(0, h[1] - 2)
    if g[0][5] == 1:
        s += 1
    if g[0][5] == 2:
        s -= 1
    if g[0][1] == 2:
        s -= 1
    return s

def fires(b):
    return score(b) >= 2

def level(b):
    return max(0, min(9, 2 * score(b) + 3))
