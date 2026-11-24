def fires(b):
    return b.grid[4][3] == 1 and b.heights[2] <= 2

def level(b):
    g = b.grid
    h2 = b.heights[2]
    if g[4][3] != 1:
        return 1 if (g[2][1] == 1 and h2 <= 1) else 0
    if h2 > 2:
        return 1
    s = 5 + (2 - h2)
    if g[2][1] == 1:
        s += 2
    return min(s, 9)
