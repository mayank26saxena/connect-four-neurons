def score4(b):
    h = b.heights
    g = b.grid
    if h[4] == 1:
        s = 3
        if g[0][4] == 1:
            s += 1
        if g[0][3] == 2:
            s += 1
        if g[0][5] == 2:
            s += 1
        if h[3] % 2 == 0:
            s += 1
        if h[5] % 2 == 0:
            s += 1
        if g[0][4] == 1 and (g[0][3] == 1 or g[0][5] == 1):
            s -= 2
        if b.ply > 24:
            s -= 2
        return max(0, min(s, 9))
    if h[4] == 3 and g[0][4] == 2 and g[1][4] == 2 and g[2][4] == 2:
        return 7
    if h[4] == 3 and g[2][4] == 2:
        return 3
    if h[4] == 2:
        return 1
    return 0

def fires(b):
    return score4(b) >= 5

def level(b):
    return score4(b)
