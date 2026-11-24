def fires(b):
    return level(b) >= 5

def level(b):
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
        return min(s, 9)
    if h[4] == 3 and g[0][4] == 2 and g[1][4] == 2 and g[2][4] == 2:
        return 7
    if h[4] == 3 and g[2][4] == 2:
        return 3
    return 0
