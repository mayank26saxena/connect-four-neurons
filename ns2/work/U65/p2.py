def _s(b):
    g = b.grid
    s = 0
    s += g[1][3] == 2
    s += g[2][3] == 1
    s += g[3][3] == 2
    s += g[1][5] == 2
    s += g[1][1] == 1
    s += g[0][2] == 2
    s -= 2 * (g[0][6] == 1)
    s -= 2 * (g[0][2] == 1)
    return s

def fires(b):
    return b.ply <= 16 and _s(b) >= 3

def level(b):
    if b.ply > 16:
        return 0
    return max(0, min(9, 2 * (_s(b) - 1)))
