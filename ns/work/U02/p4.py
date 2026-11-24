def hot(b):
    if b.ply == 0 or b.last_col is None:
        return 0
    c, r, p = b.last_col, b.last_row, b.ply
    if p == 1:
        return 9 if c == 3 else (6 if c in (0, 6) else 0)
    if p <= 10 and c == 6 and 1 <= r <= 3:
        return 6
    if p <= 7 and c == 1 and r == 0:
        return 5
    return 0

def fires(b):
    return hot(b) > 0

def level(b):
    return hot(b)
