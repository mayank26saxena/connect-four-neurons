def top(b, c):
    h = b.heights[c]
    return b.grid[h - 1][c] if h > 0 else 0

def pts(b):
    s = 0.0
    lc = b.last_col
    if lc is None:
        return 0.0
    if lc in (0, 6):
        s += 2
        if b.last_row > 0 and b.grid[b.last_row - 1][lc] == 2:
            s += 1
    t4 = top(b, 4)
    if t4 == 1:
        s += 1.5
    elif t4 == 2:
        s -= 1.5
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    return max(0, min(9, int(pts(b) * 2)))
