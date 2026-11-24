LAST = [0.0, 0.3, 0.0, 0.3, 0.5, 0.6, 0.7]

def score(b):
    if b.last_col is None:
        return -9.0
    h = b.heights
    left = 2 * (h[0] + h[2]) + h[1]
    right = h[4] + h[5] + h[6]
    return LAST[b.last_col] + 1.5 * (right - left) / b.ply - 0.02 * b.ply

def fires(b):
    return score(b) > 0.7

def level(b):
    s = score(b)
    return max(0, min(9, int((s - 0.2) / 0.15)))
