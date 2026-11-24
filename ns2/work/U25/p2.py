def _early(b):
    if b.ply > 7 or b.last_col == 4:
        return False
    if b.heights[3] + b.heights[4] > 0:
        return False
    return sum(1 for c in range(7) if b.heights[c] > 0) >= 3

def _late(b):
    if b.ply < 17 or b.last_col == 4:
        return False
    h4 = b.heights[4]
    return b.heights[3] == 6 and (h4 == 0 or h4 >= 5) and b.heights[5] <= 4

def fires(b):
    return _early(b) or _late(b)

def level(b):
    if fires(b):
        return 8
    s = 0
    if b.heights[3] in (0, 6):
        s += 2
    if b.heights[4] in (0, 5, 6):
        s += 1
    if b.last_col != 4:
        s += 1
    return s
