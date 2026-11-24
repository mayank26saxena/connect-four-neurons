def fires(b):
    return 5 <= b.ply <= 14 and b.last_row in (2, 3) and b.last_col in (1, 3, 4, 5)

def level(b):
    s = 0
    if 5 <= b.ply <= 14:
        s += 2
    if b.last_row in (2, 3):
        s += 2
    if b.last_col in (1, 4, 5):
        s += 2
    if b.grid[2][4] == 2 and b.grid[1][4] == 1:
        s += 2
    return min(9, s)
