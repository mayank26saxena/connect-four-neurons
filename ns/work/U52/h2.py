def fires(b):
    empty_center = b.heights[3] == 0 or b.heights[4] == 0
    if not empty_center:
        return False
    if b.last_col in (3, 4) and b.last_row == 0:
        return False
    return b.ply >= 1 and b.ply <= 10

def level(b):
    if not fires(b):
        return 0
    return 6 if b.ply <= 5 else 3
