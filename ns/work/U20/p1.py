def fires(b):
    if b.last_col is None or b.last_row == 0:
        return False
    return b.grid[b.last_row - 1][b.last_col] == 1 and b.ply <= 24

def level(b):
    return 5 if fires(b) else 0
