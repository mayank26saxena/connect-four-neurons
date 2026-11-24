def fires(b):
    lc = b.last_col
    lr = b.last_row
    if lc == 1:
        ok = 2 <= lr <= 4
    elif lc == 6:
        ok = 1 <= lr <= 3
    else:
        ok = False
    return ok and b.heights[2] <= 1 and b.heights[0] <= 2

def level(b):
    lc = b.last_col
    lr = b.last_row
    if lc not in (1, 6) or lr is None:
        return 0
    s = 2
    if (lc == 1 and 2 <= lr <= 4) or (lc == 6 and 1 <= lr <= 3):
        s += 3
    if b.heights[2] <= 1:
        s += 2
    if b.heights[0] <= 2:
        s += 2
    return min(9, s)
