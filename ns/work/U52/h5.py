def fires(b):
    if b.ply < 1:
        return False
    c, r = b.last_col, b.last_row
    if c == 3 and r >= 2 and b.ply <= 16:
        return True
    if c == 4 and r >= 3 and b.ply <= 16:
        return True
    if b.ply <= 9 and b.heights[3] == 0 and b.heights[4] == 0 and c in (0, 1, 2, 6):
        return True
    if b.ply >= 24 and b.heights[4] == 0:
        return True
    return False

def level(b):
    if b.ply < 1:
        return 0
    c, r = b.last_col, b.last_row
    if c in (3, 4) and r >= 3 and b.ply <= 12:
        return 9
    if fires(b):
        return 6
    if b.ply <= 9 and (b.heights[3] == 0 or b.heights[4] == 0):
        return 3
    return 0
