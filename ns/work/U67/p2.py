def o3(b):
    return sum(1 for r in range(6) if b.grid[r][3] == 2)

def fires(b):
    return b.heights[1] == 0 and b.heights[3] >= 2 and o3(b) >= 1

def level(b):
    if b.heights[1] != 0:
        return 0
    return min(9, 1 + 2 * o3(b))
