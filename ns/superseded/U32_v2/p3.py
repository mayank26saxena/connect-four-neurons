def parts(b):
    g = b.grid
    a = g[1][2] == 2 and g[2][2] == 1
    bb = g[1][4] == 1 and g[2][4] == 2
    left = b.heights[0] <= 1 and b.heights[1] <= 1
    return a, bb, left

def fires(b):
    a, bb, left = parts(b)
    return left and (a or bb)

def level(b):
    a, bb, left = parts(b)
    if not left:
        return 0
    g = b.grid
    s = 3 * a + 3 * bb
    if s == 0:
        return 1 if g[1][2] == 2 else 0
    s += (g[0][5] == 2) + (g[0][4] == 2) + (g[1][5] == 1) + (g[0][2] == 1)
    if g[0][0] == 1:
        s -= 2
    return max(0, min(9, s))
