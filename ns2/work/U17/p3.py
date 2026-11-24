def info(b):
    h = b.heights[1]
    if h < 2:
        return 0, 0
    t = h - 1
    if b.grid[t][1] != 1 or b.grid[t - 1][1] != 1:
        return 0, 0
    run = 0
    r = t
    while r >= 0 and b.grid[r][1] == 1:
        run += 1
        r -= 1
    # open neighbour cells beside the top two stones
    op = 0
    for rr in (t, t - 1):
        op += (b.grid[rr][0] == 0) + (b.grid[rr][2] == 0)
    return run, op

def fires(b):
    run, op = info(b)
    return run >= 2 and op >= 2

def level(b):
    run, op = info(b)
    if run < 2:
        return 0
    v = op + b.heights[1] - 2
    return max(0, min(9, v))
