def strength(b):
    h = b.heights
    left = 1.5 * h[0] + h[1] + h[2] + h[3]
    right = h[4] + h[5] + h[6]
    s = left - 0.2 * max(0, right - 5)
    lc = b.last_col
    if lc is not None:
        if lc <= 3:
            s += 1.0
        elif lc == 6:
            s += 0.5
        elif lc == 4:
            s -= 1.5
        else:
            s -= 0.5
    return s

def fires(b):
    return strength(b) >= 25.5

def level(b):
    s = strength(b)
    if s >= 27.5:
        return 9
    if s >= 26.5:
        return 7
    if s >= 25.5:
        return 5
    if s >= 24.5:
        return 3
    if s >= 23:
        return 1
    return 0
