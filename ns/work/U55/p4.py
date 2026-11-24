def top(b, c):
    h = b.heights[c]
    return 0 if h == 0 else b.grid[h - 1][c]

def pts(b):
    g = b.grid
    h = b.heights
    s = 0.0
    if 8 <= b.ply <= 23:
        s += 1
    elif b.ply < 6:
        s -= 2
    if h[2] in (0, 6):
        s += 1
    elif h[2] == 5:
        s += 0.5
    if 1 <= h[5] <= 4:
        s += 1
        if top(b, 5) == 2:
            s += 0.5
    if 1 <= h[6] <= 3:
        s += 1
        if top(b, 6) == 2:
            s += 0.5
        if g[0][6] == 1:
            s += 0.5
    if h[0] <= 1:
        s += 0.5
    if h[3] < 6:
        s += 0.3
    return s

def fires(b):
    p = pts(b)
    v = 0.5 + (p - 5.5) / 6.0
    return max(0.0, min(1.0, v))

def level(b):
    p = pts(b)
    return max(0, min(9, int(round((p - 3) * 3))))
