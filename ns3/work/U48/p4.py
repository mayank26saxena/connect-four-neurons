def fires(b):
    return level(b) >= 5

def level(b):
    c = b.last_col
    r = b.last_row
    p = b.ply
    if c is None:
        return 0
    if c == 4 and r == 5:
        return 7 if p >= 28 else 4
    if c == 4 and r == 0:
        return 7 if (p <= 8 or p >= 30) else 3
    if c == 2 and r == 0:
        return 6 if p <= 8 else 3
    if p <= 9 and b.heights[0] >= 3:
        return 6
    if c == 4 and r == 4 and p >= 28:
        return 4
    return 1 if p <= 7 else 0
