def fires(b):
    if b.last_col != 4:
        return False
    r = b.last_row
    return r == 0 or b.grid[r - 1][4] == 2

def level(b):
    if fires(b):
        return 8
    if b.last_col == 4:
        return 3
    return 0
