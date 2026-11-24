def fires(b):
    return b.grid[5][6] == 2

def level(b):
    if b.grid[5][6] == 2:
        s = 5
        if b.last_col == 6:
            s += 3
        if b.heights[2] <= 2:
            s += 1
        return s
    if b.grid[5][6] == 1:
        return 0
    if b.heights[6] == 5 and b.grid[4][6] == 2:
        return 2
    return 1
