def fires(b):
    c = b.last_col
    if c is None:
        return False
    r = b.last_row
    if r < 2:
        return False
    return b.grid[r][c] == 2 and b.grid[r-1][c] == 1 and b.grid[r-2][c] == 2
