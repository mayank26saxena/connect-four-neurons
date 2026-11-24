def fires(b):
    return b.last_col == 1 and b.last_row == 5

def level(b):
    if b.last_col == 1 and b.last_row is not None:
        r = b.last_row
        if r == 5:
            return 9 if b.ply >= 20 else 7
        if r == 4:
            return 4
        return 1
    return 0
