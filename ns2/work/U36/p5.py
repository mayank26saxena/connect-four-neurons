def level(b):
    h = b.heights
    g = b.grid
    if h[4] == 1:
        s = 5
        if g[0][4] == 1 and (g[0][3] == 1 or g[0][5] == 1):
            s -= 3
        if g[0][3] == 2:
            s += 1
        if g[0][5] == 2:
            s += 1
        if b.ply > 24:
            s -= 3
        return max(0, min(s, 9))
    if h[4] == 3 and g[2][4] == 2:
        return 4 if g[1][4] == 2 else 2
    if h[4] == 2:
        return 1
    return 0

def fires(b):
    return level(b) >= 5
