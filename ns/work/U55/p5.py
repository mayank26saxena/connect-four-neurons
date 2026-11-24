def top(b, c):
    h = b.heights[c]
    return 0 if h == 0 else b.grid[h - 1][c]

def pts(b):
    h = b.heights
    s = 0.0
    if b.ply < 8:
        s -= 3
    elif b.ply > 23:
        s -= 2
    s += {0: 1.3, 1: -1.4, 2: -1.4, 3: -1.4, 4: -1.4, 5: 0.0, 6: 1.3}[h[2]]
    s += {0: 0.6, 1: 0.2}.get(h[0], -0.9)
    s += {0: 0.8, 1: 0.2, 6: 0.8}.get(h[4], -0.6)
    s += {0: -1.1, 1: -0.3, 2: 0.4, 3: 1.1, 4: 0.0}.get(h[5], -2.0)
    s += {0: -0.5, 1: -0.4, 2: 0.5, 3: 1.2, 4: -0.4}.get(h[6], -1.0)
    if top(b, 5) == 2:
        s += 0.4
    if top(b, 6) == 2:
        s += 0.4
    return s

def fires(b):
    v = 0.5 + (pts(b) - 3.5) / 10.0
    return max(0.0, min(1.0, v))

def level(b):
    return max(0, min(9, int(round((pts(b) - 1.5) * 2))))
