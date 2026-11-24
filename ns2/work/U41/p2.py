WINDOWS = [[(0, 0), (1, 1), (2, 2), (3, 3)], [(1, 1), (2, 2), (3, 3), (4, 4)]]

def best(b):
    m = 0
    for w in WINDOWS:
        th = sum(1 for (r, c) in w if b.grid[r][c] == 2)
        mine = sum(1 for (r, c) in w if b.grid[r][c] == 1)
        if mine == 0 and th > m:
            m = th
    return m

def fires(b):
    return best(b) >= 3

def level(b):
    m = best(b)
    if m >= 3:
        return 9
    if m == 2:
        return 2
    return 0
