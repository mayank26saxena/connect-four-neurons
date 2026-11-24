def pts(b):
    if b.last_col is None:
        return 0
    r, c = b.last_row, b.last_col
    g = b.grid
    s = 0
    if r == 0 and c in (2, 4):
        s = 2
        o = 4 if c == 2 else 2
        if g[0][o] == 2:
            s += 1
        elif g[0][o] == 1:
            s -= 1
        if g[0][5] == 1:
            s -= 1
        if g[0][0] == 2:
            s -= 1
        if g[0][3] == 2:
            s += 1
    elif (r, c) == (5, 4):
        s = 3
    elif (r, c) == (1, 6):
        s = 3 if g[0][6] == 1 else 1
    elif (r, c) in ((4, 4), (5, 2), (1, 1)):
        s = 2
    else:
        return 0
    if b.ply <= 8:
        s += 1
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    return min(9, pts(b) * 2)
