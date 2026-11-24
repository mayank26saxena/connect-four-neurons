def est(b):
    if b.heights[2] != 1:
        return 0.0
    n1 = 0
    n2 = 0
    for c in range(7):
        if b.grid[1][c] != 0:
            n1 += 1
        for r in range(2, 6):
            if b.grid[r][c] != 0:
                n2 += 1
    e = 4.8 - 0.3 * n1 - 0.25 * n2
    if b.last_col == 2:
        return e
    if b.grid[0][2] == 2:
        return e - 1.6
    return e - 2.8

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
