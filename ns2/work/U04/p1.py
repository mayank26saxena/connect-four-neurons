def fires(b):
    if b.ply > 10:
        return False
    r, c = b.last_row, b.last_col
    if c is None:
        return False
    left = b.grid[r][c-1] if c > 0 else 0
    right = b.grid[r][c+1] if c < 6 else 0
    return left == 0 and right == 0

def level(b):
    return 6 if fires(b) else (2 if b.ply <= 10 else 0)
