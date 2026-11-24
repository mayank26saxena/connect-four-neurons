def fires(b):
    if b.ply < 1 or b.ply > 9:
        return False
    c, r = b.last_col, b.last_row
    if c in (3, 4):
        return r >= 2
    if c == 5:
        return False
    return True

def level(b):
    if not fires(b):
        return 0
    if b.last_col in (3, 4):
        return 8
    return 6 if b.ply <= 4 else 4
