def level(b):
    h = b.heights
    g = b.grid
    s = 0
    if h[4] == 1:
        s = 4
        if b.ply <= 15:
            s += 2
        elif b.ply > 22:
            s -= 3
        if h[6] == 0:
            s += 1
        elif h[6] >= 3:
            s -= 1
        if h[0] <= 1:
            s += 1
        if g[0][3] == 2 or g[0][5] == 2:
            s += 1
    elif h[4] == 3 and g[2][4] == 2 and g[1][4] == 2 and b.ply <= 18:
        s = 6
    return max(0, min(s, 9))

def fires(b):
    return level(b) >= 8
