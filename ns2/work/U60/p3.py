def fires(b):
    return level(b) >= 5

def level(b):
    c = b.last_col
    r = b.last_row
    if c is None:
        return 0
    below_mine = r > 0 and b.grid[r - 1][c] == 1
    if c == 5 and r == 1 and below_mine:
        if b.ply <= 6:
            return 9
        if b.ply <= 12:
            return 7
        return 3
    if c == 5 and r == 1:
        return 2
    if c == 2 and r == 5:
        return 5
    return 0
