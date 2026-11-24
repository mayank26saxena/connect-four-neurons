def fires(b):
    return b.heights[3] == 3 and b.heights[2] >= 4 and b.grid[3][2] == 2

def level(b):
    if not fires(b):
        return 0
    return 7
