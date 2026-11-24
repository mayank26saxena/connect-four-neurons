def points(b):
    g = b.grid
    if b.heights[3] > 2:
        return -1
    s = 0
    if g[0][3] == 2:
        s += 2
    if g[1][3] == 1:
        s += 2
    for (r, c) in [(1, 5), (0, 0), (2, 2), (2, 4), (3, 5), (2, 1)]:
        if g[r][c] == 2:
            s += 1
    if b.last_col == 3:
        s -= 2
    return s

def fires(b):
    return points(b) >= 5

def level(b):
    p = points(b)
    if p < 3:
        return 0
    return min(9, (p - 2) * 2)
