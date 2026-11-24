def fires(b):
    if b.heights[4] > 1:
        return False
    n3 = sum(1 for r in range(1, 4) if b.grid[r][3] == 1)
    return n3 >= 2

def level(b):
    if b.heights[4] > 1:
        return 0
    n3 = sum(1 for r in range(1, 4) if b.grid[r][3] == 1)
    return [0, 2, 6, 8][n3]
