def corner_score(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 0:
        s += 1
    elif g[0][0] == 1 and g[1][0] == 2 and g[2][0] == 1 and g[3][0] == 2:
        s += 3
    else:
        s -= 2
    s += {2: 2, 1: -1, 0: -2}[g[0][1]]
    s += {1: 1.5, 2: 0.5, 0: -1.5}[g[0][2]]
    if g[0][3] != 0:
        s += 0.5
    if g[0][4] != 0:
        s -= 1
    if b.ply > 12:
        s -= 1.5
    return s

def fires(b):
    return corner_score(b) >= 4

def level(b):
    s = corner_score(b)
    return max(0, min(9, int(round((s - 2) * 2))))
