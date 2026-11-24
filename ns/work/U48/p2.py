def fires(b):
    c = b.last_col
    if c is None:
        return False
    if b.ply == 1:
        return c in (3, 4, 5)
    if c == 5 and b.ply <= 3 and b.heights[5] == 1:
        return True
    if c == 4 and b.last_row >= 4:
        return True
    return False

def level(b):
    c = b.last_col
    if c is None:
        return 0
    if b.ply == 1:
        return {5: 9, 3: 6, 4: 5, 0: 2, 1: 2}.get(c, 0)
    if fires(b):
        return 6
    if c == 4 and b.last_row == 3:
        return 4
    if c == 5 and b.last_row <= 2:
        return 4
    if c == 4 or c == 6:
        return 0
    return 2
