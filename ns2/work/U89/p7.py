def score(b):
    g = b.grid
    if b.ply > 18 or g[0][4] != 2 or b.heights[1] > 1:
        return 0
    s = 1
    if g[0][5] == 1: s += 1
    if g[1][3] == 2: s += 1
    if g[2][2] == 2: s += 2
    if g[1][2] == 1: s += 1
    if g[0][0] == 2: s += 1
    if g[1][3] == 1: s -= 1
    if g[2][4] == 2: s -= 2
    if b.heights[1] == 1: s -= 1
    if b.their_playable_wins: s -= 2
    return s

def fires(b):
    return score(b) >= 2

def level(b):
    return max(0, min(9, 2 * score(b) - 2))
