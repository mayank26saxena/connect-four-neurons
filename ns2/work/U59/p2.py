def pts(b):
    h = b.heights
    s = 0
    if h[6] == 0:
        s += 1
    if h[4] <= h[3] - 1 or h[4] == 0:
        s += 1
    if h[2] > 0 and h[5] > 0:
        s += 1
    if b.ply <= 16:
        s += 1
    if len(b.my_wins) == 0:
        s += 1
    if h[0] <= 1:
        s += 1
    return s

def fires(b):
    return pts(b) >= 6

def level(b):
    return [0, 0, 0, 1, 2, 4, 8][pts(b)]
