def run0(b):
    r = b.heights[0] - 1
    n = 0
    while r >= 0 and b.grid[r][0] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return b.landing(0) is not None and run0(b) >= 3

def level(b):
    if b.landing(0) is None:
        return 0
    n = run0(b)
    if n >= 3:
        return 9 if b.heights[0] >= 4 else 7
    if n == 2 and b.last_col == 0:
        return 1
    return 0
