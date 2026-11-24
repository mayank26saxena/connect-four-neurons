def fires(b):
    return b.grid[0][3] == 2 and b.heights[6] <= 2

def level(b):
    if not fires(b):
        return 0
    s = 3
    if b.grid[0][6] == 2:
        s += 2
    if b.grid[1][4] == 2:
        s += 2
    return s
