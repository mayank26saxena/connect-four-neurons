def top(b, c):
    h = b.heights[c]
    return b.grid[h - 1][c] if h > 0 else 0

def pts(b):
    if b.last_col is None:
        return 0
    s = 0
    t4 = top(b, 4)
    if t4 == 1:
        s += 1
        if b.heights[4] in (2, 3):
            s += 1
    elif t4 == 2:
        s -= 1
    if b.heights[6] >= 2 and top(b, 6) == 2:
        s += 2
    if b.last_col in (0, 6):
        s += 1
    if b.heights[1] == 0:
        s += 0.5
    if b.heights[5] == 0:
        s += 0.5
    return s

def fires(b):
    return pts(b) >= 3.5

def level(b):
    return max(0, min(9, int(pts(b) * 1.5)))
