def pts(b):
    g = b.grid
    h = b.heights
    s = 0.0
    if g[0][6] == 1 and g[1][6] == 2:
        s += 2
    if h[2] == 0:
        s += 1.5
    elif h[2] == 6:
        s += 2.5
    elif h[2] == 5:
        s += 1.5
    elif h[2] == 4:
        s += 0.5
    else:
        s -= 1
    for c in (0, 4):
        if 0 < h[c] < 6:
            s -= 0.5 * sum(1 for r in range(h[c]) if g[r][c] == 2)
    if b.ply < 6:
        s -= 2
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    p = pts(b)
    return max(0, min(9, int(round((p - 1) * 2))))
