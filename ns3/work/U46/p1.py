def col0_run(b):
    h = b.heights[0]
    if h == 0 or h >= 6:
        return 0
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][0] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return col0_run(b) >= 3

def level(b):
    n = col0_run(b)
    if n >= 3:
        return 9 if b.last_col == 0 else 6
    if n == 2:
        return 1
    return 0
