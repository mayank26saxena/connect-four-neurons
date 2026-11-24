def bonus(b):
    h = b.heights
    s = 0
    if b.last_col == 6:
        s += 1
    if h[2] <= 3:
        s += 1
    if h[4] >= 5:
        s += 1
    if h[5] >= 5:
        s += 1
    return s

def fires(b):
    return b.grid[5][6] == 2 and bonus(b) >= 2

def level(b):
    if b.grid[5][6] == 2:
        return min(9, 3 + bonus(b) + bonus(b) // 2)
    if b.grid[5][6] == 1:
        return 2 if b.grid[4][6] == 2 else 0
    return 1
