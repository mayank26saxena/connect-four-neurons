def est(b):
    if b.last_col != 0:
        return 0.0
    h = b.heights[0]
    if h <= 2:
        return 0.3 * h
    base = [0, 0, 0, 2.8, 6.8, 8.5, 9.3][h]
    p = b.ply
    e = base + 3.1 - 0.25 * max(p, 16) - 0.15 * max(0, 16 - p)
    pen = [0, 1.9, 1.55, 0.5, 0.5, 0.8, 1.1]
    for c in range(1, 7):
        if b.heights[c] == 6:
            e = e - pen[c]
    return e

def fires(b):
    return est(b) >= 2.1

def level(b):
    e = est(b)
    return max(0, min(9, int(round(e * 1.2))))
