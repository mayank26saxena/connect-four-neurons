def fires(b):
    h = b.heights[3]
    if any(x == 6 for x in b.heights):
        return False
    if h == 2 and b.grid[1][3] == 2:
        return True
    if h == 4 and b.grid[1][3] == 2 and b.grid[3][3] == 1:
        return True
    return False

def level(b):
    if fires(b):
        return 6 if b.ply <= 14 else 3
    return 0
