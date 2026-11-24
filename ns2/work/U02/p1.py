def fires(b):
    if b.last_col is None or b.last_row != 0:
        return False
    if b.last_col == 3:
        return b.ply >= 8
    return b.ply >= 12 and b.last_col in (1, 5, 6)

def level(b):
    if b.last_col is None or b.last_row != 0:
        return 0
    if b.last_col == 3:
        if b.ply >= 12:
            return 9
        if b.ply >= 8:
            return 6
        return 2
    if b.ply >= 12:
        return 4
    return 1
