def fires(b):
    return b.grid[4][3] == 1

def level(b):
    g = b.grid
    s = 0
    if g[4][3] == 1:
        s += 5
    if g[2][1] == 1:
        s += 2
    if g[1][1] == 1:
        s += 1
    if b.heights[2] <= 1:
        s += 1
    return min(s, 9)
