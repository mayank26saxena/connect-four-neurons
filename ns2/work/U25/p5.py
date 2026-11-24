def _early(b):
    if b.ply > 7 or b.last_col == 4:
        return False
    if b.heights[3] + b.heights[4] > 0:
        return False
    return sum(1 for c in range(7) if b.heights[c] > 0) >= 3

def _late(b):
    if b.ply < 17 or b.last_col == 4:
        return False
    if b.heights[3] != 6 or b.heights[5] >= 5:
        return False
    theirs3 = sum(1 for r in range(6) if b.grid[r][3] == 2)
    return theirs3 >= 4 or b.last_col == 3

def fires(b):
    return _early(b) or _late(b)

def level(b):
    if fires(b):
        return 8
    h = b.heights
    s = 0
    if h[3] == 6 or (h[3] == 0 and h[4] == 0):
        s += 3
    if b.last_col != 4:
        s += 1
    if not (8 <= b.ply <= 16):
        s += 2
    return s
