LAST = [0.1, 0.35, 0.05, 0.35, 0.5, 0.65, 0.7]

def score(b):
    if b.last_col is None:
        return -9.0
    h = b.heights
    left = 2 * (h[0] + h[2]) + h[1]
    right = h[4] + h[5] + h[6]
    s = LAST[b.last_col] + 1.5 * (right - left) / b.ply - 0.02 * b.ply
    if b.last_col >= 4 and b.last_row >= 2:
        s -= 0.7 * (b.last_row - 1)
    if h[0] == 0 and h[2] == 0:
        s += 0.25
    return s

def fires(b):
    return score(b) > 0.8

def level(b):
    s = score(b)
    return max(0, min(9, int((s - 0.3) / 0.15)))
