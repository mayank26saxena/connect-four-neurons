def fires(b):
    h = b.heights[3]
    if b.last_col is None or b.last_col == 3:
        return False
    if h < 1 or h > 2:
        return False
    return 2 <= b.last_row <= 3

def level(b):
    if b.last_col is None or b.last_col == 3:
        return 0
    h = b.heights[3]
    if h < 1 or h > 2:
        return 0
    s = 0
    if 2 <= b.last_row <= 3:
        s += 5
    if b.grid[h - 1][3] == 1:
        s += 3
    return s
