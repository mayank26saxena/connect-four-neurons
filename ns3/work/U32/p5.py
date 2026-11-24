def fires(b):
    h = b.heights
    return h[1] == 1 and h[0] >= 2 and h[2] >= 2 and h[3] >= 3

def level(b):
    h = b.heights
    if h[1] != 1:
        return 0
    s = 2 + min(h[0], 2) + min(h[2], 3) + (2 if h[3] >= 3 else 0)
    return min(9, s)
