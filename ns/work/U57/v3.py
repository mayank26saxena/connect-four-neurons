def top_run(b, c):
    # number of opponent stones stacked at the top of column c (0 if top is mine or empty)
    h = b.heights[c]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    if b.landing(1) is not None and top_run(b, 1) >= 3:
        return True
    if b.landing(5) is not None and top_run(b, 5) >= 3 and b.ply <= 22:
        return True
    return False

def level(b):
    if b.landing(1) is not None:
        k = top_run(b, 1)
        if k >= 3:
            return 9
        if k == 2:
            return 2
    if b.landing(5) is not None and top_run(b, 5) >= 3 and b.ply <= 22:
        return 1
    return 0
