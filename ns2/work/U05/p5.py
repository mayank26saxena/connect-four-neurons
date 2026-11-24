def nb(b):
    n = 0
    for c in (3, 5):
        for r in (1, 2, 3):
            if b.grid[r][c] != 0:
                n += 1
    return n

def strength(b):
    if b.heights[4] != 2:
        return -1
    s = nb(b)
    if b.heights[5] >= 2:
        s += 1
    if b.last_col == 4:
        s += 2
    return s

def fires(b):
    return strength(b) >= 5

def level(b):
    s = strength(b)
    if s < 0:
        return 0
    return min(9, 1 + s)
