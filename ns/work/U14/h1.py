def fires(b):
    return b.heights[4] == 4 and b.grid[3][4] == 1

def level(b):
    if fires(b):
        return 7
    h = b.heights[4]
    if h > 0 and b.grid[h - 1][4] == 1:
        return 2
    return 0
