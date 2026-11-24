def fires(b):
    if b.heights[2] != 1:
        return False
    if b.last_col == 2:
        return b.ply <= 12
    if b.grid[0][2] == 2:
        return b.ply <= 9
    return b.ply <= 7

def level(b):
    if b.heights[2] != 1:
        return 0
    p = b.ply
    if b.last_col == 2:
        return 9 if p <= 6 else (8 if p <= 8 else (6 if p <= 12 else 3))
    s = 5 if p <= 6 else (4 if p <= 9 else (2 if p <= 14 else 1))
    if b.grid[0][2] == 2:
        s += 1
    return s
