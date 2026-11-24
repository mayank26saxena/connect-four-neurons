LASTW = [-0.15, -0.25, -0.6, -0.6, -0.6, -0.4, 0.0]

def score(b):
    p = b.ply
    if p < 28:
        return -1.0
    s = 1.75 + 0.12 * (p - 34)
    if p % 2 == 1:
        s -= 0.7
    if b.last_col is not None:
        s += LASTW[b.last_col]
    return s

def fires(b):
    return score(b) > 1.167

def level(b):
    s = score(b)
    v = int((s - 0.2) / 0.25)
    return max(0, min(9, v))
