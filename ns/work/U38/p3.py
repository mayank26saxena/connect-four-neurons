W_OPP = {0: 0.4, 1: 0.25, 2: -0.1, 3: 0.45, 4: 0.6, 5: 0.55}

def score(b):
    g = b.grid
    if g[0][6] != 1:
        return -1.0
    s = 0.0
    for r in range(1, 6):
        if g[r][6] == 2:
            s -= 1.2
        elif g[r][6] == 1:
            s += 0.2
    for c in range(6):
        if g[0][c] == 2:
            s += W_OPP[c]
        elif g[0][c] == 1 and c in (4, 5):
            s -= 0.4
    s -= 0.08 * max(0, b.ply - 5)
    return s

def fires(b):
    return score(b) > 0.45

def level(b):
    s = score(b)
    if s <= 0:
        return 0
    return max(1, min(9, int(s * 6)))
