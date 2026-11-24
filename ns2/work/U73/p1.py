def _score(b):
    if b.last_col is None:
        return -9
    w = {0: 3.0, 1: 3.5, 2: 1.0, 3: 1.3, 4: 0.5, 5: 1.8, 6: 0.0}[b.last_col]
    p = b.ply
    if p == 4:
        bonus = 0.0
    elif p == 5:
        bonus = -1.3
    elif p == 6:
        bonus = -1.6
    elif p == 8:
        bonus = -2.0
    else:
        bonus = -2.5 - 0.1 * (p - 8)
    return w + bonus

def fires(b):
    return _score(b) >= 1.0

def level(b):
    s = _score(b)
    if s < 0.5:
        return 0
    return max(0, min(9, int(round(s * 2.4))))
