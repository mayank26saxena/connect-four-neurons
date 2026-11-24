def shape(b):
    if b.heights[4] > 1:
        return 0
    s = 0
    for r in range(1, 3):
        if b.grid[r][2] == 1 and b.grid[r][3] == 1:
            s += 1
    if b.heights[2] == 2 and b.grid[1][2] == 1 and b.grid[0][3] == 2:
        s += 1
    return s

def fires(b):
    return shape(b) >= 1

def level(b):
    s = shape(b)
    return 0 if s == 0 else min(9, 4 + 2 * s)
