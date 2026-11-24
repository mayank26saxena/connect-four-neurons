def fires(b):
    g = b.grid
    return g[2][2] == 2 and g[1][3] == 2

def level(b):
    g = b.grid
    s = 0
    for (r, c) in [(2, 2), (1, 3), (2, 1), (3, 1), (1, 2), (0, 4)]:
        if g[r][c] == 2:
            s += 2
    return min(9, s) if fires(b) else min(3, s // 2)
