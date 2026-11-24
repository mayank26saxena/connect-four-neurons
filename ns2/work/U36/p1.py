def fires(b):
    return b.heights[4] == 1

def level(b):
    if b.heights[4] == 1:
        return 6 if b.grid[0][4] == 1 else 4
    return 0
