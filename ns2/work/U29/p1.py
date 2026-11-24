def fires(b):
    return b.grid[4][3] == 2 and b.grid[4][4] == 0 and b.grid[3][4] != 1

def level(b):
    s = 0
    if b.grid[4][3] == 2:
        s += 4
    if b.grid[4][4] == 0:
        s += 2
    if b.grid[3][4] != 1:
        s += 1
    if b.grid[5][3] != 2:
        s += 1
    if b.heights[3] - b.heights[4] >= 2:
        s += 1
    return min(9, s) if b.grid[4][3] == 2 and b.grid[4][4] == 0 else min(2, s // 3)
