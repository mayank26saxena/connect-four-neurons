LINE = [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]

def best(b):
    m = 0
    for s in (0, 1):
        w = LINE[s:s + 4]
        if any(b.grid[r][c] == 1 for (r, c) in w):
            continue
        n = sum(1 for (r, c) in w if b.grid[r][c] == 2)
        m = max(m, n)
    return m

def fires(b):
    return best(b) >= 2

def level(b):
    n = best(b)
    return [0, 1, 6, 9, 9][n]
