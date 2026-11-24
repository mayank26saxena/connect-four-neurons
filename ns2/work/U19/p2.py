def fires(b):
    h = b.heights[4]
    if h == 6:
        return b.grid[5][4] == 2 and b.grid[4][4] == 1
    if h == 2:
        return b.grid[1][4] == 2 and b.grid[0][4] == 1
    return False
