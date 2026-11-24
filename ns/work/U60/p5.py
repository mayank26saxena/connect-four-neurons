LASTW = [0.1, -0.15, -0.4, -0.3, -0.3, 0.0, 0.3]

def score(b):
    p = b.ply
    if p < 26:
        return 0.0
    if p % 2 == 0:
        base = 1.25 + 0.2 * (p - 34)
    else:
        base = 1.25 + 0.2 * (p - 39)
    return base + LASTW[b.last_col]

def fires(b):
    return score(b) > 1.167

def level(b):
    s = score(b)
    v = int(s / 0.3)
    return max(0, min(9, v))
