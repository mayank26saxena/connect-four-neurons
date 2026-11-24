def s(b):
    g = b.grid
    v = 0
    v += 2 if g[0][3] == 2 else 0
    v += 1 if g[1][3] == 2 else 0
    v += 2 if g[1][4] == 2 else 0
    v += 2 if g[2][5] == 2 else 0
    v += 1 if g[2][4] == 1 else 0
    return v

def fires(b):
    return s(b) >= 7

def level(b):
    v = s(b)
    if v < 4:
        return 0
    if v < 6:
        return 1
    if v < 7:
        return 3
    if v < 8:
        return 5 if b.ply < 24 else 6
    return 7 if b.ply < 24 else 9
