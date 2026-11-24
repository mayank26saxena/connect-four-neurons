def well_depth(b):
    h = b.heights
    best = 0
    for c in range(7):
        left = h[c - 1] if c > 0 else 0
        right = h[c + 1] if c < 6 else 0
        d = min(left, right) - h[c] if 0 < c < 6 else 0
        best = max(best, d)
    return best

def fires(b):
    full = sum(1 for x in b.heights if x == 6)
    return full == 0 and well_depth(b) >= 2

def level(b):
    full = sum(1 for x in b.heights if x == 6)
    s = 2 * well_depth(b) - 2 * full
    return max(0, min(9, s))
