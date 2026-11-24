def score(b):
    g = b.grid
    s = 0.0
    if g[0][4] == 2: s += 2.0
    elif g[0][4] == 1: s -= 1.0
    if g[1][3] == 2: s += 1.0
    if g[2][2] == 2: s += 1.0
    if g[0][3] == 2: s += 0.8
    if g[0][0] == 2: s += 0.5
    if g[0][5] == 1: s += 0.5
    for (r, c) in ((1, 3), (2, 2), (3, 1)):
        if g[r][c] == 1: s -= 0.8
    if b.their_playable_wins: s -= 2.0
    h1 = b.heights[1]
    f = [1.0, 0.6, 0.45, 0.3, 0.25, 0.2, 0.2][h1]
    return s * f if s > 0 else s

def fires(b):
    return score(b) >= 2.5

def level(b):
    s = score(b)
    if s < 1.5:
        return 0
    return max(0, min(9, int((s - 1.5) * 2.5)))
