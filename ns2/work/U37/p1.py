def fires(b):
    if b.ply > 10:
        return False
    if b.heights[3] < 2:
        return False
    if any(b.grid[r][0] == 1 for r in range(6)):
        return False
    return True

def level(b):
    if not fires(b):
        return 0
    return max(1, 9 - (b.ply - 4))
