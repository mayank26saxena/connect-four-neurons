def s(b):
    g = b.grid
    v = 0
    for (r, c) in [(2, 4), (2, 5), (3, 3), (3, 2), (1, 4)]:
        if g[r][c] == 2:
            v += 1
        elif g[r][c] == 1:
            v -= 1
    for (r, c) in [(0, 2), (3, 4), (2, 3)]:
        if g[r][c] == 1:
            v += 1
        elif g[r][c] == 2:
            v -= 1
    return v

def fires(b):
    return s(b) >= 4

def level(b):
    return max(0, min(9, 2 * s(b) - 3))
