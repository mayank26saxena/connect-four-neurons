def gap(b):
    return b.heights[5] == 0 and b.heights[4] >= 1 and b.heights[6] >= 1

def fires(b):
    return gap(b) and b.last_col in (4, 6, 2, 0)

def level(b):
    s = 0
    if gap(b):
        s += 4
    if b.last_col == 4:
        s += 4
    elif b.last_col == 5:
        s += 1
    return min(9, s)
