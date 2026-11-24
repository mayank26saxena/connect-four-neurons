def fires(b):
    h = b.heights[4]
    if h < 2:
        return False
    return b.grid[h-1][4] == 2 and b.grid[h-2][4] == 1
