def vthree6(b):
    h = b.heights[6]
    if h < 3 or h >= 6:
        return 0
    if all(b.grid[h - 1 - k][6] == 2 for k in range(3)):
        return h
    return 0

def fires(b):
    return vthree6(b) > 0

def level(b):
    h = vthree6(b)
    if h == 3:
        return 9
    if h == 4:
        return 7
    if h == 5:
        return 6
    if b.last_col == 6 and b.heights[6] >= 2 and b.grid[b.heights[6] - 1][6] == 2 and b.grid[b.heights[6] - 2][6] == 2:
        return 2
    return 0
