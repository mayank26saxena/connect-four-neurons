def fires(b):
    g = b.grid
    a = g[2][4] == 2 and g[1][4] == 1
    lr = b.last_row
    c = b.last_col
    bb = lr == 2 and c in (0, 1, 4, 5) and g[1][c] != 0
    return a or bb

def level(b):
    g = b.grid
    s = 0
    if g[2][4] == 2 and g[1][4] == 1:
        s += 4
        if b.last_col == 4:
            s += 3
    if b.last_row == 2 and b.last_col in (0, 1, 4, 5):
        s += 3
    if g[0][5] == 1:
        s += 1
    return min(9, s)
