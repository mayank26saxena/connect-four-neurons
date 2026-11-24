def run0(b):
    h = b.heights[0]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][0] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    if b.landing(0) is None:
        return False
    n = run0(b)
    if n >= 3:
        return True
    return n == 2 and b.last_col == 0

def level(b):
    if b.landing(0) is None:
        return 0
    n = run0(b)
    if n >= 3:
        return 9 if b.heights[0] >= 4 else 8
    if n == 2:
        return 2 if b.last_col == 0 else 1
    return 0
