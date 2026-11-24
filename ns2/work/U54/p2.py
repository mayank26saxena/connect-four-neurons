def fires(b):
    h = b.heights
    if h[5] == 0 or b.grid[h[5] - 1][5] != 2:
        return False
    return h[4] <= 1 and h[5] >= h[4] + 1

def level(b):
    h = b.heights
    s = 0
    if h[5] > 0 and b.grid[h[5] - 1][5] == 2:
        s += 3
    if h[4] <= 1:
        s += 3
    if h[5] > h[4]:
        s += min(3, h[5] - h[4])
    return min(9, s)
