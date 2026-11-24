def fires(b):
    return b.heights[4] <= 1 and b.grid[1][2] == 1 and b.heights[2] == 2

def level(b):
    return 7 if fires(b) else 0
