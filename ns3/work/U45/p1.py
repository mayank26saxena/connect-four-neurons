def fires(b):
    if b.last_col is None:
        return False
    c, r = b.last_col, b.last_row
    if c == 4 and r == 0 and b.ply <= 5:
        return True
    if c == 5 and r in (2, 3):
        return True
    return False

def level(b):
    if b.last_col is None:
        return 0
    c, r = b.last_col, b.last_row
    if c == 4 and r == 0:
        return 9 if b.ply <= 5 else 4
    if c == 5 and r == 2:
        return 6
    if c == 5 and r == 3:
        return 5
    if (c, r) in ((0, 3), (1, 3), (3, 4), (2, 1)):
        return 3
    return 0
