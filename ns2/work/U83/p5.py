def points(b):
    g = b.grid
    h = b.heights[3]
    if h > 2:
        return -5
    s = 0
    if h == 2 and g[0][3] == 2 and g[1][3] == 1:
        s += 4
    elif h >= 1 and g[h - 1][3] == 1:
        s += 2
    if b.last_col == 3:
        s -= 3
    if g[0][0] == 2:
        s += 1
    if g[0][6] == 1:
        s += 1
    if g[0][2] == 2:
        s -= 1
    for (r, c) in [(1, 5), (2, 2), (2, 4), (3, 5)]:
        if g[r][c] == 2:
            s += 1
    if b.ply <= 7:
        s += 1
    if b.ply >= 22:
        s -= 2
    return s

def fires(b):
    return points(b) >= 5

def level(b):
    p = points(b)
    if p < 3:
        return 0
    return min(9, (p - 2) * 2)
