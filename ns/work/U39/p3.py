def score(b):
    h = b.heights
    g = b.grid
    s = 0
    if h[3] == 0:
        s += 1
    elif h[3] <= 2:
        s -= 2
    elif h[3] in (4, 5):
        s += 2
    elif h[3] == 6:
        s -= 1
    if h[2] >= 3:
        s += 1
    if h[2] >= 4:
        s += 1
    if h[3] == 0 and h[1] >= 3:
        s += 1
    if h[1] == 6 or h[2] == 6:
        s -= 2
    for c in (4, 5, 6):
        s -= max(0, h[c] - 1)
    if g[0][5] == 1:
        s += 1
    if g[0][5] == 2:
        s -= 1
    return s

def fires(b):
    return score(b) >= 3

def level(b):
    return max(0, min(9, 2 * score(b)))
