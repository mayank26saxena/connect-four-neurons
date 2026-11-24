def win_ok(b, r, c0):
    n = 0
    for c in range(c0, c0 + 4):
        v = b.grid[r][c]
        if v == 1:
            return -1
        if v == 2:
            n += 1
    return n

def best(b):
    if b.last_col is None:
        return 0
    r = b.last_row
    c = b.last_col
    if r < 1:
        return 0
    m = 0
    for c0 in range(max(0, c - 3), min(3, c) + 1):
        m = max(m, win_ok(b, r, c0))
    return m

def fires(b):
    return best(b) >= 2

def level(b):
    m = best(b)
    return [0, 0, 5, 8, 9][m]
