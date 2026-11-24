def fires(b):
    c = b.last_col
    r = b.last_row
    if c is None:
        return False
    if c == 5 and r == 1 and b.grid[0][5] == 1:
        return True
    if c == 2 and r == 5:
        return True
    return False

def level(b):
    if not fires(b):
        return 0
    if b.last_col == 5:
        return 9 if b.ply <= 8 else 5
    return 5
