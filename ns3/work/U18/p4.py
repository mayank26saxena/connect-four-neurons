def fires(b):
    if b.last_col != 4:
        return False
    if b.last_row == 0:
        return True
    return b.last_row == 1 and b.grid[0][4] == 2 and b.ply >= 8

def level(b):
    if b.last_col != 4:
        return 0
    if b.last_row == 0:
        return 9 if b.ply <= 24 else 7
    if b.last_row == 1 and b.grid[0][4] == 2:
        return 5 if b.ply >= 8 else 3
    return 1 if b.last_row == 1 else 0
