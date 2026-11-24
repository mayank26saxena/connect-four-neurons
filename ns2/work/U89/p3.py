def rowscore(b, r):
    g = b.grid
    if g[r][3] != 2 or g[r][4] != 2:
        return 0.0
    s = 2.0
    if g[r][5] == 1:
        s += 2.0
    elif g[r][5] == 2:
        s -= 1.0
    if g[r][2] == 2:
        s -= 1.0
    return s

def score(b):
    best = 0.0
    for r in range(6):
        best = max(best, rowscore(b, r))
    if best == 0:
        return 0.0
    if b.their_playable_wins:
        best -= 2.0
    h1 = b.heights[1]
    best *= [1.0, 0.8, 0.65, 0.5, 0.4, 0.3, 0.3][h1]
    return best

def fires(b):
    return score(b) >= 2.5

def level(b):
    s = score(b)
    if s < 1.0:
        return 0
    return max(0, min(9, int(s * 2)))
