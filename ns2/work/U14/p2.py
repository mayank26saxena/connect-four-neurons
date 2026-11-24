def fires(b):
    c = b.last_col
    if c is None or b.last_row != 2:
        return False
    if c == 3:
        return True
    return c in (2, 4, 5) and b.grid[1][c] == 1

def level(b):
    c = b.last_col
    if c is None:
        return 0
    if fires(b):
        s = 6
        if b.grid[0][c] == 1 and b.grid[1][c] == 1:
            s += 2
        if b.ply <= 10:
            s += 1
        return s
    if b.last_row == 2:
        return 3
    return 0
