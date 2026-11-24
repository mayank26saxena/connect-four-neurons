def fires(b):
    c = b.last_col
    if c is None or b.last_row != 2:
        return False
    if b.grid[1][c] != 1:
        return False
    return 2 <= c <= 5 and max(b.heights) <= 3

def level(b):
    c = b.last_col
    if c is None:
        return 0
    if fires(b):
        return 8 if b.grid[0][c] == 1 else 7
    s = 0
    if b.last_row == 2:
        s += 3
        if b.grid[1][c] == 1:
            s += 1
    if max(b.heights) <= 3:
        s += 1
    return s
