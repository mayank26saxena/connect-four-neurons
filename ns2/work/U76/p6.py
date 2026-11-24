def fires(b):
    h = b.heights
    return b.grid[4][3] == 1 and h[2] <= 2 and h[4] >= 4

def level(b):
    g = b.grid
    h = b.heights
    s = 0
    if g[4][3] == 1:
        s = 2
        if h[2] <= 2:
            s += 2
            if h[4] >= 4:
                s += 3
            if h[2] == 0:
                s += 1
            if g[2][1] == 1:
                s += 1
    return min(s, 9)
