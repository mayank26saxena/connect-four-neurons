def pairs(b):
    n = 0
    for r in range(1, 4):
        if b.grid[r][2] == 1 and b.grid[r][3] == 1 and b.grid[r][4] == 0:
            n += 1
    return n

def fires(b):
    return pairs(b) >= 1

def level(b):
    p = pairs(b)
    if p == 0:
        return 0
    return 5 + 2 * p - (1 if b.heights[4] > 1 else 0)
