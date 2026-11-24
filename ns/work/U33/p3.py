def score(b):
    g = b.grid
    s = 0.0
    if g[0][6] == 2:
        s += 1.5
        if g[1][6] == 2:
            s += 1.0
            if g[2][6] == 2:
                s += 1.5
    if g[0][2] == 1:
        s += 1.0
    if g[0][3] == 1:
        s += 0.7
    if g[1][3] == 1:
        s += 0.5
    if g[0][5] == 2:
        s -= 1.0
    if g[0][4] == 2:
        s -= 0.7
    if g[0][4] == 1:
        s -= 0.7
    if g[0][1] != 0:
        s -= 0.6
    if b.ply > 16:
        s -= 1.0
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 2.0:
        return 0
    return max(0, min(9, int(round((s - 2.0) * 2.5))))
