def fires(b):
    p = b.ply
    c = b.last_col
    if p == 1:
        return c == 1
    if p == 4 or p == 5:
        return c == 3
    if p >= 24 and p % 2 == 0:
        return c in (3, 4, 5, 6)
    return False

def level(b):
    p = b.ply
    c = b.last_col
    if p == 4 and c == 3:
        return 9
    if fires(b):
        return 5
    if c == 3:
        return 2
    return 0
