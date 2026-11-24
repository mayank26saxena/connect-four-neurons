def level(b):
    h = b.heights
    g = b.grid
    if h[4] == 1:
        s = 5
        if g[0][3] == 2:
            s += 1
        if g[0][5] == 2:
            s += 1
        if g[0][4] == 1 and (g[0][3] == 1 or g[0][5] == 1):
            s -= 2
        if h[6] == 0:
            s += 1
        if b.ply % 2 == 1:
            s += 1
        if b.ply > 22:
            s -= 3
        elif b.ply > 16:
            s -= 1
    elif h[4] == 3 and g[2][4] == 2:
        s = 6 if g[1][4] == 2 else 3
        if b.ply > 20:
            s -= 2
    elif h[4] == 2 or h[4] == 0:
        s = 1
    else:
        s = 0
    return max(0, min(s, 9))

def fires(b):
    return level(b) >= 7
