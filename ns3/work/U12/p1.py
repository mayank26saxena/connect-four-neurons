def val(b):
    if b.last_col != 0:
        return -9.0
    return b.heights[0] - b.ply / 9.0

def fires(b):
    return val(b) >= 1.4

def level(b):
    v = val(b)
    if v < -1:
        return 0
    return max(0, min(9, int(round((v + 0.6) * 2.5))))
