def well(b):
    h = b.heights
    if h[2] > 1:
        return 0
    s = h[1] + h[3] + h[0] // 2 - 3 * h[2] - (h[4] + h[5] + h[6]) // 2
    if h[3] < 4 or h[1] < 2:
        return 0
    return s

def fires(b):
    if b.ply == 1 and b.last_col == 0:
        return True
    return well(b) >= 8

def level(b):
    if b.ply == 1 and b.last_col == 0:
        return 3
    s = well(b)
    if s < 5:
        return 0
    return min(9, s - 4)
