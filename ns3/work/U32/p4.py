def fires(b):
    h = b.heights
    return h[1] == 1 and h[0] >= 1 and 12 <= b.ply <= 26 and h[2] + h[3] >= 7

def level(b):
    h = b.heights
    if h[1] > 1:
        return 1 if b.ply >= 30 else 0
    s = 1
    if h[1] == 1: s += 2
    if h[0] >= 1: s += 1
    if 12 <= b.ply <= 26: s += 2
    if h[2] + h[3] >= 7: s += 2
    return s
