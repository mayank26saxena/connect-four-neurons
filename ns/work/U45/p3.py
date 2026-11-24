def points(b):
    g = b.grid
    s = 0.0
    if b.heights[2] == 0:
        s += 3
    elif b.heights[2] == 1:
        s += 1
    if b.heights[1] == 0:
        s += 1
    if g[0][3] == 1:
        s += 1
    if g[1][3] == 2:
        s += 1
    if g[2][3] == 1:
        s += 1
    for r in range(1, 6):
        if g[r][4] == 2:
            s -= 1.5
        elif g[r][4] == 1:
            s += 0.5
    if b.heights[0] > 0:
        s += 0.5
    if b.ply < 6:
        s -= 3
    return s

def fires(b):
    return points(b) >= 5.5

def level(b):
    p = points(b)
    if p < 4.5:
        return 0
    return max(0, min(9, int(round((p - 4.5) * 2.5))))
