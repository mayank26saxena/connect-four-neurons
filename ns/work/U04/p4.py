def bonus(b):
    s = 0
    if b.last_col == 6:
        s += 2
    if b.heights[2] <= 3:
        s += 2
    if b.heights[4] == 6:
        s += 1
    return s

def fires(b):
    return b.grid[5][6] == 2 and bonus(b) >= 2

def level(b):
    if b.grid[5][6] == 2:
        return 3 + bonus(b) + (1 if b.heights[2] <= 1 else 0)
    if b.grid[5][6] == 1:
        return 2 if b.grid[4][6] == 2 else 0
    return 1
