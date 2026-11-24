def tscore(b):
    g = b.grid
    s = 0
    s += 2 * (g[1][5] == 2)
    s += 2 * (g[0][5] == 1)
    s += (g[0][4] == 1)
    s += (g[0][3] == 2)
    s += (g[0][2] == 2)
    s += (g[1][3] == 2)
    s -= 2 * (g[1][4] == 1)
    return s

def fires(b):
    return tscore(b) >= 5

def level(b):
    s = tscore(b)
    return max(0, min(9, 2 * (s - 3))) if s > 3 else 0
