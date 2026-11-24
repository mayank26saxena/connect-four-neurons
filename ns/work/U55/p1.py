def fires(b):
    h = b.heights
    if b.ply < 7:
        return False
    if h[2] not in (0, 5, 6):
        return False
    if h[0] > 1:
        return False
    return h[4] in (0, 1, 6)

def level(b):
    return 6 if fires(b) else 0
