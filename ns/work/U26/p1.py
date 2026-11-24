def score(b):
    g = b.grid
    s = 0.0
    if g[0][4] == 2: s += 2
    if g[1][4] == 2: s += 1
    if g[0][3] == 2: s += 1
    if g[1][3] == 2: s += 1.5
    if g[0][2] == 1: s += 1.5
    if g[2][2] == 1: s += 1
    if g[0][3] == 1: s -= 1.5
    if g[1][4] == 1: s -= 1.5
    if g[0][4] == 1: s -= 1.5
    s -= 0.1 * b.ply
    s -= 0.5 * (b.heights[5] + b.heights[6] + max(0, b.heights[4] - 2))
    return s

def fires(b):
    return score(b) >= 3.5

def level(b):
    v = score(b)
    return max(0, min(9, int(round((v - 1) * 2))))
