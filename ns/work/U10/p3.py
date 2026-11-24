def pts(b):
    g = b.grid
    s = 0
    for r in range(6):
        for c in (0, 1):
            if g[r][c] == 2:
                s += 1
            elif g[r][c] == 1:
                s -= 1
        if g[r][3] == 1:
            s += 1
        elif g[r][3] == 2:
            s -= 1
    s -= 3 * b.heights[2]
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    s = pts(b)
    if s < 0:
        return 0
    return min(9, s * 2)
