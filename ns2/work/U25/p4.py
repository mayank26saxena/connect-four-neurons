def fires(b):
    h = b.heights
    if b.last_col == 4 or 8 <= b.ply <= 16:
        return False
    if h[3] == 6:
        return h[4] == 0 or h[4] >= 5
    return h[3] == 0 and h[4] == 0

def level(b):
    h = b.heights
    s = 0
    if h[3] == 6 or (h[3] == 0 and h[4] == 0):
        s += 4
    if b.last_col != 4:
        s += 2
    if not (8 <= b.ply <= 16):
        s += 2
    if b.last_col == 5:
        s += 1
    return s
