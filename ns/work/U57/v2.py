def top_run(b, c):
    # number of opponent stones stacked at the top of column c
    n = 0
    r = b.heights[c] - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return b.landing(1) is not None and top_run(b, 1) >= 3

def level(b):
    if b.landing(1) is not None:
        k = top_run(b, 1)
        if k >= 3:
            return 9
        if k == 2:
            return 1
    return 0
