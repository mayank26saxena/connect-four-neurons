def strength(b):
    h = b.heights
    left = h[0] + h[1] + h[2] + h[3]
    right = h[4] + h[5] + h[6]
    s = left - 0.25 * max(0, right - 8)
    lc = b.last_col
    if lc is not None:
        if lc <= 3:
            s += 1.0
        elif lc in (4, 5):
            s -= 1.5
    return s

def fires(b):
    return strength(b) >= 22.5

def level(b):
    s = strength(b)
    if s >= 24.5:
        return 9
    if s >= 23.5:
        return 7
    if s >= 22.5:
        return 5
    if s >= 21.5:
        return 3
    if s >= 20:
        return 1
    return 0
