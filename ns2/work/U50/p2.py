def fires(b):
    if b.last_col == 4 and b.heights[5] == 0:
        return True
    if b.last_col == 5 and b.heights[4] == 0:
        return True
    return False

def level(b):
    s = 0
    if b.last_col == 4:
        s += 4
    if b.last_col == 5:
        s += 2
    if b.heights[5] == 0:
        s += 3
    elif b.heights[5] <= 1:
        s += 1
    if b.heights[4] == 0:
        s += 1
    return min(9, s)
