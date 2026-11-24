def fires(b):
    h = b.heights
    return h[0] == 0 and h[4] == 0 and h[1] > 0 and h[2] > 0 and h[3] > 0

def level(b):
    if not fires(b):
        return 0
    s = 5
    if b.grid[0][1] == 2:
        s += 2
    if b.grid[0][2] == 1:
        s += 1
    return s
