def fires(b):
    h = b.heights[3]
    if h < 1 or h > 2 or b.last_col == 3:
        return False
    return b.grid[h - 1][3] == 1

def level(b):
    if not fires(b):
        return 0
    if b.heights[3] == 2 and b.grid[0][3] == 2:
        return 8
    return 5
