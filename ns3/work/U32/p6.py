def fires(b):
    h = b.heights
    if h[1] > 1 or h[0] < 1:
        return False
    if h[1] == 1:
        return 12 <= b.ply <= 26 and h[2] + h[3] >= 7
    return 4 <= b.ply <= 14

def level(b):
    h = b.heights
    if h[1] > 1:
        return 1 if b.ply >= 30 else 0
    s = 1
    if h[0] >= 1: s += 2
    if 10 <= b.ply <= 26: s += 2
    if h[2] + h[3] >= 7: s += 2
    if h[1] == 1: s += 1
    return s
