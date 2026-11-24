def counts(b):
    t = 0
    m = 0
    for r, c in ((1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 3), (3, 5)):
        v = b.grid[r][c]
        if v == 2:
            t += 1
        elif v == 1:
            m += 1
    return t, m

def fires(b):
    if b.heights[4] != 2:
        return False
    t, m = counts(b)
    return t - m >= 2

def level(b):
    if b.heights[4] != 2:
        return 0
    t, m = counts(b)
    s = 3 + 2 * (t - m)
    if b.last_col == 4:
        s += 1
    return max(0, min(s, 9))
