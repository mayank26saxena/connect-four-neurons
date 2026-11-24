def pts(b):
    h = b.heights
    g = b.grid
    s = 0.0
    s += {0: -2.0, 1: 1.0, 2: 1.2, 3: 0.0, 4: 0.3}.get(h[4], -2.5)
    if g[0][0] == 2: s += 0.8
    if g[0][4] == 2: s += 0.8
    if g[0][0] == 2 and g[0][4] == 2: s += 0.8
    if h[1] == 0: s += 0.6
    if h[5] == 0: s += 0.6
    # opponent's vertical stack in column 6
    if h[6] >= 3 and g[h[6] - 1][6] == 2 and g[h[6] - 2][6] == 2:
        s += 1.0
        if g[h[6] - 3][6] == 2: s += 0.8
    for r in range(6):
        for c in (1, 3, 5):
            if g[r][c] == 2: s -= 0.15
        for c in (0, 2, 6):
            if g[r][c] == 2: s += 0.1
    if b.last_col in (0, 6): s += 0.5
    if b.ply > 28: s -= 1.0
    return s

def fires(b):
    return pts(b) >= 4.0

def level(b):
    return max(0, min(9, int(round((pts(b) - 1.5) * 2))))
