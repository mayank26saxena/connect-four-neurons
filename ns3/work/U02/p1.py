def fires(b):
    h = b.heights
    if h[0] < 6 or h[3] < 6:
        return False
    full = sum(1 for c in range(7) if h[c] == 6)
    return full >= 4

def level(b):
    h = b.heights
    full = sum(1 for c in range(7) if h[c] == 6)
    if h[0] < 6 or h[3] < 6:
        return min(3, full)
    return min(9, 2 * full - 2)
