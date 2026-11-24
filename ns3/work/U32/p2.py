def fires(b):
    h = b.heights
    return h[1] == 1 and h[3] >= 4 and h[0] >= 1 and h[2] >= 1

def level(b):
    h = b.heights
    if h[1] != 1:
        return 0
    s = 2
    if h[3] >= 4: s += 3
    if h[0] >= 1: s += 2
    if h[2] >= 1: s += 2
    return s
