def level(b):
    h = b.heights
    g = b.grid
    s = 0
    if h[4] == 1:
        s = 2
        if g[0][3] == 2:
            s += 2
        if g[0][5] == 2:
            s += 2
        if g[0][4] == 1 and g[0][5] == 1:
            s -= 2
        if g[0][4] == 1 and g[0][3] == 1:
            s -= 2
        if b.ply % 2 == 1:
            s += 1
    elif h[4] == 3 and g[2][4] == 2 and g[1][4] == 2:
        s = 5
    return max(0, min(s, 9))

def fires(b):
    return level(b) >= 5
