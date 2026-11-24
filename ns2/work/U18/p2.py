def fires(b):
    h2 = b.heights[2]
    if h2 < 1 or h2 > 4:
        return False
    return b.grid[h2 - 1][2] == 1 and b.heights[4] <= 2

def level(b):
    return 6 if fires(b) else 0
