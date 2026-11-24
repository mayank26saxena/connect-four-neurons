def top(b, c):
    h = b.heights[c]
    return b.grid[h - 1][c] if h > 0 else 0

def fires(b):
    return b.last_col in (3, 6) and b.ply >= 9 and top(b, 4) == 1

def level(b):
    s = 0
    if b.ply >= 9:
        s += 1
    if b.last_col in (3, 6):
        s += 3
    if top(b, 4) == 1:
        s += 3
        if b.heights[4] == 4:
            s += 2
    return min(s, 9)
