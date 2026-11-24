W = {
    (1, 6, 2): 2, (2, 6, 2): 2, (0, 6, 1): 1,
    (1, 3, 1): 1, (1, 4, 1): 1, (0, 3, 2): 1, (0, 4, 2): 1,
    (0, 2, 1): 1, (1, 2, 2): 1, (0, 0, 2): 1,
    (0, 1, 0): 1, (0, 5, 0): 0.5,
}

def pts(b):
    if b.last_col is None:
        return 0
    s = 0
    for (r, c, v), w in W.items():
        if b.grid[r][c] == v:
            s += w
    if b.last_col in (3, 4) and b.heights[b.last_col] <= 3:
        s -= 1.5
    if b.last_col == 6:
        s += 1
    s -= max(0, b.ply - 20) * 0.15
    return s

def fires(b):
    return pts(b) >= 5.5

def level(b):
    return max(0, min(9, int(pts(b) - 1)))
