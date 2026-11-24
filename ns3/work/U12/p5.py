def est(b):
    if b.last_col != 0:
        return -5.0
    o = 0
    x = 0
    for r in range(b.heights[0]):
        if b.grid[r][0] == 2:
            o += 1
        else:
            x += 1
    e = 1.3 * o + 0.9 * min(x, o) - 0.8 * max(0, x - o) + 0.6
    if x == 0:
        e = e - 3.0
    p = b.ply
    e = e - 0.25 * max(0, p - 16) - 0.15 * max(0, 16 - p)
    return e

def fires(b):
    return est(b) >= 2.1

def level(b):
    e = est(b)
    return max(0, min(9, int(round(e * 1.25))))
