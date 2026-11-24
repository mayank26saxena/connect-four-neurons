def capped(b):
    c = b.last_col
    r = b.last_row
    if c is None or r is None or r < 1:
        return False
    return c in (2, 3, 4) and b.grid[r - 1][c] == 1

def fires(b):
    return capped(b) and b.ply <= 16

def level(b):
    s = 0
    if capped(b):
        s += 4
    if b.ply <= 12:
        s += 3
    elif b.ply <= 18:
        s += 1
    if b.grid[0][3] == 2:
        s -= 2
    return max(0, min(9, s))
