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
        if b.ply <= 6:
            return 9
        if b.ply <= 12:
            return 8
        if b.ply <= 20:
            return 7
        return 6
    if b.last_row == 1 and b.grid[0][4] == 2:
        if b.ply >= 16:
            return 6
        if b.ply >= 12:
            return 5
        return 3
    return 1 if b.last_row == 1 else 0
