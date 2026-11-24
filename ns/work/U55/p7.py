def top(b, c):
    h = b.heights[c]
    return 0 if h == 0 else b.grid[h - 1][c]

def pts(b):
    h = b.heights
    g = b.grid
    s = 0.0
    if b.ply < 8:
        s -= 3
    elif b.ply > 23:
        s -= 2
    # column 2 untouched or completely full
    s += {0: 1.3, 5: 0.0, 6: 1.3}.get(h[2], -1.4)
    # columns 0 and 4 low (col 4 full also fine)
    s += {0: 0.6, 1: 0.2}.get(h[0], -0.9)
    s += {0: 0.8, 1: 0.2, 6: 0.8}.get(h[4], -0.6)
    # columns 5 and 6 part-filled, about 3 and 2-3 high
    s += {0: -1.1, 1: -0.3, 2: 0.4, 3: 1.1, 4: 0.0}.get(h[5], -2.0)
    s += {0: -0.5, 1: -0.4, 2: 0.5, 3: 1.2, 4: -0.4}.get(h[6], -1.0)
    if top(b, 5) == 2:
        s += 0.4
    # column 6: my stone at the bottom, theirs on top
    t6 = top(b, 6)
    if t6 == 2:
        s += 0.6
    elif t6 == 1:
        s -= 0.6
    if g[0][6] == 1:
        s += 0.6
    elif g[0][6] == 2:
        s -= 0.6
    return s

def fires(b):
    v = 0.5 + (pts(b) - 2.8) / 20.0
    return max(0.0, min(1.0, v))

def level(b):
    return max(0, min(9, int(round((pts(b) - 1.0) * 2))))
