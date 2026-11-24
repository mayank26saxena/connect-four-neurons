def fires(b):
    return b.grid[2][3] == 1 and b.heights[4] == 0

def level(b):
    s = 0
    if b.grid[2][3] == 1:
        s += 4
    if b.heights[4] == 0:
        s += 3
    elif b.heights[4] == 1 and b.grid[0][4] == 1:
        s += 1
    if b.heights[3] >= 2 and b.heights[3] <= 5:
        s += 1
    return min(9, s)
