CELL = {(0, 2): 3, (0, 4): 3, (5, 4): 3, (1, 6): 3, (4, 4): 2, (5, 2): 2, (1, 1): 2}

def pts(b):
    if b.last_col is None:
        return 0
    cell = (b.last_row, b.last_col)
    s = CELL.get(cell, 0)
    if s == 0:
        return 0
    g = b.grid
    if cell[0] == 0:
        if g[0][2] == 2 and g[0][4] == 2:
            s += 1
        if g[0][5] == 1:
            s -= 1
        if g[0][0] == 2:
            s -= 1
    if b.ply <= 8:
        s += 1
    return s

def fires(b):
    return pts(b) >= 4

def level(b):
    return min(9, pts(b) * 2)
