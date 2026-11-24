def pts(b):
    if b.last_col is None:
        return 0
    r, c = b.last_row, b.last_col
    g = b.grid
    if (r, c) in ((0, 2), (0, 4), (5, 4)):
        s = 3
    elif (r, c) == (1, 6) and g[0][6] == 1:
        s = 3
    elif (r, c) in ((4, 4), (5, 2), (1, 1), (1, 6)):
        s = 2
    else:
        return 0
    s -= sum(1 for k in range(6) if g[k][0] == 2)
    if g[0][5] == 1:
        s -= 1
    if b.ply <= 8:
        s += 1
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    return max(0, min(9, pts(b) * 2))
