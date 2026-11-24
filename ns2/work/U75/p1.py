def fires(b):
    h = b.heights[2]
    if h == 0:
        return True
    if h == 2 and b.grid[1][2] == 2:
        return True
    return False

def level(b):
    return 6 if fires(b) else 0
