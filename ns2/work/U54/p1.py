def fires(b):
    h = b.heights
    return h[4] <= 1 and max(h[3], h[5]) >= 3

def level(b):
    h = b.heights
    if h[4] > 1:
        return 0
    d = max(h[3], h[5]) - h[4]
    return max(0, min(9, 2 * d))
