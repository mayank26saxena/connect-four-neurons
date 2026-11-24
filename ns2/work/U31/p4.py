def high(b):
    n = 0
    for r in range(2, 6):
        for c in range(7):
            if b.grid[r][c] != 0:
                n += 1
    return n

def est(b):
    if b.heights[2] != 1:
        return 0.0
    e = 4.5 - 0.15 * (b.ply - 4) - 0.2 * high(b)
    if b.last_col == 2:
        return e
    if b.grid[0][2] == 2:
        return e - 1.4
    return e - 2.6

def fires(b):
    return est(b) > 1.83

def level(b):
    e = est(b)
    cuts = [0.37, 0.73, 1.17, 1.55, 1.83, 2.15, 3.23, 3.89, 4.62]
    n = 0
    for t in cuts:
        if e > t:
            n += 1
    return n
