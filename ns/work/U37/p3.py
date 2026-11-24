def score(b):
    # opponent stone at (1,2) on top of column 2 (height 2), landing cell (2,2) empty
    if b.heights[2] != 2 or b.grid[1][2] != 2:
        return None
    g = b.grid
    s = 0.0
    if b.last_col == 2:
        s += 2
    if g[2][3] == 2:
        s -= 2
    if g[2][1] == 2:
        s -= 0.5
    if g[1][1] == 1:
        s += 1
    if g[1][3] == 1:
        s += 1
    return s

def fires(b):
    s = score(b)
    return s is not None and s >= 1

def level(b):
    s = score(b)
    if s is None:
        return 0
    return max(1, min(9, int(round(3 + 1.5 * s))))
