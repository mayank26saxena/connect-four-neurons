def est(b):
    high = 0
    for r in range(2, 6):
        for c in range(7):
            if b.grid[r][c] != 0:
                high += 1
    e = 4.5 - 0.15 * (b.ply - 4) - 0.2 * high
    if b.heights[2] != 1:
        return 0.0
    if b.last_col == 2:
        return e
    e = e - 2.0
    if b.grid[0][2] == 2:
        e += 0.4
    return e

def fires(b):
    return est(b) > 1.8

def level(b):
    e = est(b)
    cuts = [0.37, 0.73, 1.17, 1.55, 1.83, 2.15, 3.23, 3.89, 4.62]
    n = 0
    for t in cuts:
        if e > t:
            n += 1
    return n
