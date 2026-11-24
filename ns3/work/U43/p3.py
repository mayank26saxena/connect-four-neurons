def fires(b):
    g = b.grid
    return g[2][1] == 2 and g[3][1] == 2 and g[4][1] != 1

def level(b):
    g = b.grid
    if not fires(b):
        if g[2][1] == 2 and g[3][1] == 0:
            return 2
        if g[2][1] == 2 and g[3][1] == 2:
            return 2
        return 0
    s = 4
    if g[4][1] == 2:
        s += 3
        if g[5][1] == 0:
            s += 1
    if g[1][1] == 2:
        s += 1
    return min(s, 9)
