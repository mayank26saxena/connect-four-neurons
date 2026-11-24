def fires(b):
    return b.grid[1][2] == 2 and b.heights[0] <= 1 and b.heights[1] <= 1

def level(b):
    if b.grid[1][2] != 2:
        return 0
    s = 4
    s -= max(0, b.heights[1] - 1) * 2
    s -= max(0, b.heights[0] - 1)
    if b.grid[0][3] == 2:
        s += 2
    if b.grid[2][2] == 1:
        s += 2
    return max(0, min(9, s))
