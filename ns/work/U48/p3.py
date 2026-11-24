def fires(b):
    c = b.last_col
    if c is None:
        return False
    h = b.heights
    r = b.last_row
    if b.ply == 1:
        return c in (3, 4, 5)
    if b.ply <= 3:
        return c == 5 and h[5] == 1 and h[0] == 0 and h[4] == 0 and h[6] == 0
    if c == 4:
        return r >= 4 and h[5] + h[6] <= 5 and h[0] <= 3
    if c == 5:
        return r <= 2 and h[4] <= 2 and h[2] + h[3] >= 6
    if c in (1, 2, 3):
        return h[4] <= 2 and h[2] + h[3] >= 10
    return False

def level(b):
    c = b.last_col
    if c is None:
        return 0
    if b.ply == 1:
        return {5: 9, 3: 6, 4: 5, 0: 2, 1: 2}.get(c, 0)
    if fires(b):
        return 6
    if c == 4 and b.last_row >= 3:
        return 4
    if c == 5 and b.last_row <= 2:
        return 4
    if c == 4 or c == 6:
        return 0
    return 2
