def fires(b):
    c = b.last_col
    r = b.last_row
    if c == 4 and (r == 5 or r == 0):
        return True
    if b.heights[0] >= 3 and b.ply <= 12 and c in (0, 2, 4):
        return True
    if c == 2 and r == 0:
        return True
    return False

def level(b):
    if not fires(b):
        return 0
    if b.heights[0] >= 4 and b.ply <= 10:
        return 9
    return 5
