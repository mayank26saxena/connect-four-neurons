W_OPP = [0.35, 0.25, -0.25, 0.4, 0.45, 0.5, -1.2]
W_ME = [-0.1, -0.1, 0.05, -0.2, -0.5, -0.5, 0.1]

def score(b):
    g = b.grid
    if g[0][6] != 1:
        return -1.0
    s = -0.1
    for c in range(7):
        for r in range(6):
            if (r, c) == (0, 6):
                continue
            if g[r][c] == 2:
                s += W_OPP[c] * (1.0 if r == 0 else 0.6)
            elif g[r][c] == 1:
                s += W_ME[c] * (1.0 if r == 0 else 0.6)
    s -= 0.04 * max(0, b.ply - 4)
    return s

def fires(b):
    return score(b) > 0.55

def level(b):
    s = score(b)
    if s <= 0:
        return 0
    return max(1, min(9, int(s * 6)))
