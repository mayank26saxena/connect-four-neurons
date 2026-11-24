def fires(b):
    h = b.heights
    if h[4] != 4:
        return False
    if b.grid[3][4] != 1:
        return False
    left = h[0] + h[1] + h[2]
    return left <= 4 and h[5] <= 3 and h[3] >= 2

def level(b):
    h = b.heights
    s = 0
    if h[4] == 4:
        s += 3
        if b.grid[3][4] == 1:
            s += 2
        if b.grid[2][4] == 1:
            s += 1
    left = h[0] + h[1] + h[2]
    if left <= 4:
        s += 2
    if h[5] <= 3:
        s += 1
    return min(s, 9)
