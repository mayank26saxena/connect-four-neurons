def n_opp(b):
    g = b.grid
    return sum(1 for (r, c) in [(0, 3), (0, 5), (1, 3), (1, 4)] if g[r][c] == 2)

def ok(b):
    g = b.grid
    if b.heights[5] != 1 or b.heights[4] < 1 or b.heights[3] < 1:
        return False
    if g[1][3] == 1:
        return False
    return g[0][5] == 2 or (g[1][3] == 2 and g[1][4] == 2)

def fires(b):
    if not ok(b):
        return False
    s = n_opp(b) + (1 if b.grid[0][6] == 1 else 0) + (1 if b.ply < 12 else 0)
    return s >= 3

def level(b):
    if not ok(b):
        return 0
    s = n_opp(b) + (1 if b.grid[0][6] == 1 else 0) + (1 if b.ply < 12 else 0)
    return [0, 1, 2, 5, 7, 9, 9][s]
