def fires(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return False
    if p in (5, 7):
        return c <= 4
    if p == 6:
        return c == 3
    if p >= 37:
        return c >= 5
    return False

def level(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return 0
    if p == 5:
        return 8 if c <= 4 else 2
    if p == 7:
        return 6 if c <= 4 else 1
    if 19 <= p <= 28:
        return 4 if c <= 3 else 1
    if p >= 34:
        return 6 if c >= 5 else 2
    return 0
