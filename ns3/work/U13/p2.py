def vert(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def diag_threat6(b):
    # opponent completes a diagonal four by playing the landing cell of column 6
    r = b.landing(6)
    if r is None:
        return False
    for dr in (1, -1):
        cells = [(r - dr * k, 6 - k) for k in range(1, 4)]
        if all(0 <= rr < 6 and b.grid[rr][cc] == 2 for rr, cc in cells):
            return True
    return False

def fires(b):
    if vert(b, 6):
        return True
    if b.last_col is not None and b.last_col != 6 and vert(b, b.last_col):
        return True
    return diag_threat6(b) and b.last_col == 6

def level(b):
    if vert(b, 6):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if diag_threat6(b) and b.last_col == 6:
        return 3
    if b.last_col is not None and vert(b, b.last_col):
        return 1
    return 0
