def fires(b):
    h = b.heights[3]
    return h in (1, 2) and b.last_col != 3

def level(b):
    if not fires(b):
        return 0
    if b.heights[3] == 2 and b.grid[0][3] == 2 and b.grid[1][3] == 1:
        return 8
    return 4
