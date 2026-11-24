def score(b):
    g = b.grid
    s = 0.0
    if 4 <= b.ply <= 12:
        s += 1.0
    elif b.ply > 16:
        s -= 1.0
    if g[0][3] == 2:
        s -= 1.0
    if g[0][3] == 1:
        s += 0.5
    if g[1][3] == 1:
        s += 0.5
    if g[0][0] == 2 or g[0][1] == 2:
        s += 0.5
    if b.last_col == 2:
        s += 0.5
    return s

def fires(b):
    return score(b) >= 2.0

def level(b):
    return max(0, min(9, int(round(2 * (score(b) + 1.0)))))
