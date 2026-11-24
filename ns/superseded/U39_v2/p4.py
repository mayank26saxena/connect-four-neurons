def _core(b):
    h = b.heights
    right = h[4] + h[5] + h[6]
    centre = h[2] + h[3]
    return right, centre

def fires(b):
    if not (8 <= b.ply <= 16) or b.last_col in (1, 2):
        return False
    right, centre = _core(b)
    return right <= 3 and centre >= 5

def level(b):
    if b.ply < 6 or b.ply > 18 or b.last_col in (1, 2):
        return 0
    right, centre = _core(b)
    s = centre - 2 * right
    if b.last_col in (0, 6):
        s += 1
    return max(0, min(9, s - 1))
