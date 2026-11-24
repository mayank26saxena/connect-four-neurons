def hot(b):
    if b.ply == 0 or b.last_col is None:
        return 0
    c, r, p = b.last_col, b.last_row, b.ply
    if p == 1:
        return 9 if c == 3 else (6 if c in (0, 6) else 0)
    if p <= 9:
        if c == 6 and r in (1, 2):
            return 6
        if c == 0 and r <= 1:
            return 5
        if c == 1 and r == 0:
            return 6
        if c == 3 and r == 2:
            return 5
        if c == 4 and r == 3:
            return 5
        return 0
    if r >= 4 and c in (0, 1, 4, 6):
        return 6 if r == 5 else 5
    return 0

def fires(b):
    return hot(b) > 0

def level(b):
    return hot(b)
