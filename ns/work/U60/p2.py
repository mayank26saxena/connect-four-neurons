LASTW = [-0.15, -0.25, -0.6, -0.6, -0.6, -0.4, 0.0]
COLW = [0.0, -0.1, 0.0, 0.08, 0.2, -0.2, 0.06]

def score(b):
    p = b.ply
    s = 2.3 + 0.12 * (p - 38)
    if p % 2 == 1:
        s -= 0.8
    if b.last_col is not None:
        s += LASTW[b.last_col]
    for c in range(7):
        s += COLW[c] * (b.heights[c] - p / 7.0)
    return s

def fires(b):
    return score(b) > 1.167

def level(b):
    s = score(b)
    v = int((s - 0.2) / 0.25)
    return max(0, min(9, v))
