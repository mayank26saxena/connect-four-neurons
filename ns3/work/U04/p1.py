def top_run(b, c):
    h = b.heights[c]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return b.landing(0) is not None and top_run(b, 0) >= 3

def level(b):
    if b.landing(0) is None:
        return 0
    n = top_run(b, 0)
    if n >= 3:
        return 9
    if n == 2:
        return 2
    return 0
