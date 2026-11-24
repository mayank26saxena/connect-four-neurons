def _k(b):
    h = b.heights
    return sum([h[1] == 0, h[5] == 0, h[3] in (3, 4), h[4] == 3, h[6] in (2, 4), h[0] == 1])

def fires(b):
    return _k(b) >= 3

def level(b):
    return min(9, 2 * _k(b))
