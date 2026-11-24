W_OPP = {0: 0.5, 1: 0.3, 2: -0.2, 3: 0.5, 4: 0.65, 5: 0.6, 6: 0.0}

def score(b):
    g = b.grid
    s = -0.5
    if g[0][6] == 1:
        s += 1.0
        if g[1][6] == 2:
            s -= 1.0
        elif g[1][6] == 1:
            s += 0.3
    elif g[0][6] == 2:
        s -= 0.3
    for c in range(6):
        if g[0][c] == 2:
            s += W_OPP[c]
            if g[1][c] == 2:
                s += 0.3
        elif g[0][c] == 1 and c in (4, 5):
            s -= 0.5
    for c in (4, 5):
        if g[1][c] == 1:
            s -= 0.4
    s -= 0.04 * max(0, b.ply - 6)
    return s

def fires(b):
    return score(b) > 0.6

def level(b):
    s = score(b)
    if s <= 0:
        return 0
    return max(0, min(9, int(s * 5)))
