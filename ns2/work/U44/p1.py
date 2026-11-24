def fires(b):
    c = b.last_col
    r = b.last_row
    if c is None or r is None or r < 1:
        return False
    return b.grid[r - 1][c] == 2 and c in (0, 1, 4, 5)

def level(b):
    c = b.last_col
    r = b.last_row
    if c is None or r is None or r < 1:
        return 0
    if b.grid[r - 1][c] == 2:
        return 8 if c in (1, 5) else (5 if c in (0, 4) else 2)
    return 2 if c in (1, 4, 5) else 0
