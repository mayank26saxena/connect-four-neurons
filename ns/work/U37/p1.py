def fires(b):
    return b.heights[2] == 2 and b.grid[1][2] == 2

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.last_col == 2:
        s += 3
    if b.grid[1][1] == 1:
        s += 1
    if b.grid[1][3] == 1:
        s += 1
    return min(s, 9)
