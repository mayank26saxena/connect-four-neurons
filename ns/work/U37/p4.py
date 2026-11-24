def score(b):
    # opponent stone at (1,2) on top of column 2 (height 2): landing cell (2,2) empty
    if b.heights[2] != 2 or b.grid[1][2] != 2:
        return None
    g = b.grid
    s = 0
    for (r, c) in ((1, 1), (1, 3), (2, 1), (2, 3), (3, 1), (3, 3)):
        if g[r][c] == 1:
            s += 1
        elif g[r][c] == 2:
            s -= 1
    if b.last_col == 2:
        s += 1
    if b.ply < 6:
        s -= 1
    return s

def fires(b):
    s = score(b)
    return s is not None and s >= 1

def level(b):
    s = score(b)
    if s is None:
        return 0
    return max(1, min(9, 4 + s))
