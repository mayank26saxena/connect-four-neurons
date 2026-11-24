def late(b):
    h = b.heights
    return h[4] == 6 and (h[5] == 6 or h[3] == 6) and h[1] < 6 and h[2] < 6

def fires(b):
    return late(b)

def level(b):
    h = b.heights
    if h[4] < 6:
        return 0
    s = 2
    if h[5] == 6:
        s += 1
    if h[3] == 6:
        s += 1
    if h[1] < 6 and h[2] < 6:
        s += 2
    if h[0] == 6 or h[6] == 6:
        s += 1
    if b.ply >= 27:
        s += 1
    return min(9, s)
