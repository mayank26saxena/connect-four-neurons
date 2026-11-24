def fires(b):
    if b.last_col is None:
        return False
    return b.ply <= 6 and b.last_col >= 4 and b.heights[3] <= 1

def level(b):
    if b.last_col is None:
        return 0
    lv = 0
    if b.last_col == 5:
        lv += 4
    elif b.last_col in (4, 6):
        lv += 3
    lv += max(0, 5 - abs(b.ply - 4))
    if b.heights[3] >= 2:
        lv -= 2
    return max(0, min(9, lv))
