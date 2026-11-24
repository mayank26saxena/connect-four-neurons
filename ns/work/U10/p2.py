def pts(b):
    h = b.heights
    if h[2] > 1:
        return 0
    s = h[0] + h[1] + h[3] - 3 * h[2] - (h[4] + h[5] + h[6]) // 2
    if b.last_col in (0, 1, 3):
        s += 3
    return s

def fires(b):
    return pts(b) >= 12

def level(b):
    s = pts(b)
    if s < 6:
        return 0
    return int(min(9, (s - 6) // 2 + 1))
