def score(b):
    g = b.grid
    if b.heights[1] > 1 or b.their_playable_wins:
        return 0
    m1 = g[0][3] == 2 and g[0][4] == 2 and g[0][5] == 1 and g[0][2] != 2
    m2 = g[2][2] == 2 and g[1][2] == 1
    if not (m1 or m2):
        return 0
    s = 2 if (m1 and m2) else 1
    for (r, c) in ((0, 0), (0, 3), (0, 4), (1, 3), (1, 4), (2, 2)):
        if g[r][c] == 2:
            s += 1
    if g[0][5] == 1: s += 1
    if b.heights[1] == 1: s -= 1
    if b.ply > 20: s -= 2
    return s

def fires(b):
    return score(b) >= 4

def level(b):
    return max(0, min(9, 2 * score(b) - 4))
