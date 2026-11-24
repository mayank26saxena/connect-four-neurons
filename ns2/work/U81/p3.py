def col(b, c):
    return [b.grid[r][c] for r in range(b.heights[c])]

def score(b):
    g = b.grid
    s = 0.0
    c5 = col(b, 5)
    if c5[:4] == [1, 1, 2, 2]:
        s += 2.0
        if len(c5) == 5 and c5[4] == 2:
            s += 1.0
    c4 = col(b, 4)
    if c4[:4] == [1, 1, 2, 2]:
        s += 1.5
    c1 = col(b, 1)
    if len(c1) >= 5 and c1[1:5] == [1, 1, 1, 2]:
        s += 2.0
    c6 = col(b, 6)
    if c6 == [2]:
        s += 1.0
    if g[0][2] == 1:
        s += 0.7
    if g[0][3] == 2:
        s += 0.5
    if g[0][4] == 1:
        s += 0.4
    if g[0][5] == 1:
        s -= 0.8
    if b.ply > 26:
        s -= 1.0
    return s

def fires(b):
    return score(b) >= 2.0

def level(b):
    s = score(b)
    if s < 1.0:
        return 0
    return max(0, min(9, int(2 * s - 1)))
