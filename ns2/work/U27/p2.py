def fires(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return False
    if p in (5, 7):
        return c <= 4
    if p >= 36:
        return c >= 5
    return False

def level(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return 0
    if p == 5:
        return (9 if c == 3 else 7) if c <= 4 else 2
    if p == 7:
        return (7 if c == 3 else 5) if c <= 4 else 1
    if p >= 32:
        return 6 if c >= 5 else 1
    if 19 <= p <= 28:
        return 3 if c <= 3 else 0
    return 0
