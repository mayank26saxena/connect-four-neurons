def est(b):
    if b.last_col != 0:
        return 0.0
    h = b.heights[0]
    if h <= 1:
        return 0.0
    if h == 2:
        return 0.5
    e = 1.6 * h - 0.22 * max(b.ply, 16) + 1.4
    if h == 3:
        e = e - 0.9
    return e

def fires(b):
    return est(b) >= 2.2

def level(b):
    e = est(b)
    return max(0, min(9, int(round(e * 1.3))))
