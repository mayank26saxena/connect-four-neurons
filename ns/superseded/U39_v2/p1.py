def fires(b):
    h = b.heights
    return h[2] + h[3] >= 6 and h[4] + h[5] + h[6] <= 3

def level(b):
    h = b.heights
    s = (h[2] + h[3]) - 2 * (h[4] + h[5] + h[6])
    return max(0, min(9, s - 1))
