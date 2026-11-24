def fires(b):
    if b.last_row is None:
        return False
    return b.last_row == 5 or (b.last_row == 4 and b.last_col in (0, 6))

def level(b):
    if b.last_row is None:
        return 0
    r = b.last_row
    if r == 5:
        return 9 if b.last_col in (0, 6) else 6
    if r == 4:
        return 4 if b.last_col in (0, 6) else 2
    return 0
