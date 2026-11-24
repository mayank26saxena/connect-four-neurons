def bonus(b):
    h = b.heights
    s = 0
    if b.last_col == 6:
        s += 1
    if h[2] <= 3:
        s += 1
    if h[4] >= 5:
        s += 1
    if h[5] >= 5:
        s += 1
    return s

def weight(b):
    # column 6 must be full; opponent stone on top counts 2, opponent stone just below counts 1
    if b.heights[6] < 6:
        return -1
    return 2 * (b.grid[5][6] == 2) + (b.grid[4][6] == 2) + bonus(b)

def fires(b):
    return weight(b) >= 4

def level(b):
    w = weight(b)
    if w < 0:
        return 1
    return min(9, w + w // 2)
