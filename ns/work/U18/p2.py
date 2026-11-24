def score(b):
    g = b.grid
    s = 0.0
    if g[0][3] == 1: s += 1.0
    if g[0][3] == 2: s -= 1.5
    if g[1][3] == 1: s += 1.0
    if g[0][5] == 1: s += 0.8
    if g[0][1] == 2: s += 0.6
    # their stone capping my stone in the centre columns
    for c in (2, 3, 4):
        h = b.heights[c]
        if h >= 2 and g[h - 1][c] == 2 and g[h - 2][c] == 1:
            s += 1.0
    if b.last_col == 2:
        s += 0.5
    s -= 0.08 * b.ply
    return s

def fires(b):
    return score(b) >= 1.6

def level(b):
    v = int(round((score(b) - 0.0) * 3))
    return max(0, min(9, v))
