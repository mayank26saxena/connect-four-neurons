def fires(b):
    return b.heights[3] == 4 and b.grid[3][3] == 2

def level(b):
    if not fires(b):
        return 0
    s = 3
    if b.grid[2][3] == 2:
        s += 3
        if b.grid[1][3] == 2:
            s += 1
    if b.last_col == 3:
        s += 2
    return min(9, s)
