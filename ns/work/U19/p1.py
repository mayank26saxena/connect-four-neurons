def fires(b):
    return b.grid[1][5] == 2

def level(b):
    if b.grid[1][5] != 2:
        return 0
    s = 3
    if b.grid[0][5] == 1:
        s += 2
    if b.heights[4] <= 1:
        s += 2
    return min(s, 9)
