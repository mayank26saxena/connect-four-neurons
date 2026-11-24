def fires(b):
    return b.last_col == 4 and b.last_row == 0

def level(b):
    if b.last_col != 4:
        return 0
    if b.last_row != 0:
        return 2 if b.last_row == 1 else 0
    if b.ply <= 6:
        return 9
    if b.ply <= 12:
        return 8
    if b.ply <= 20:
        return 7
    return 6
