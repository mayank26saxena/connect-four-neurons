def fires(b):
    # opponent's last stone landed on top of another of their stones in a central column
    c, r = b.last_col, b.last_row
    if c is None or r is None or r == 0:
        return False
    return c in (2, 3, 4) and b.grid[r - 1][c] == 2

def level(b):
    c, r = b.last_col, b.last_row
    if c is None or r is None or r == 0:
        return 0
    s = 0
    if b.grid[r - 1][c] == 2:
        s += 3
        if r >= 2 and b.grid[r - 2][c] == 2:
            s += 2
    if c == 3:
        s += 3
    elif c in (2, 4):
        s += 1
    return min(9, s)
