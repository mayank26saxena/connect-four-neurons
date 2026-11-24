def est(b):
    if b.last_col != 0:
        return 0.0
    r = b.last_row
    h1, h2 = b.heights[1], b.heights[2]
    if r == 4:
        base = 4.2
    elif r == 3:
        base = 2.8
    elif r == 5:
        return 2.0 if h1 == 6 else 0.0
    else:
        return 0.0
    return base - 0.3 * max(h1, h2) - 0.15 * min(h1, h2)

def fires(b):
    return est(b) > 0.8

def level(b):
    e = est(b)
    if e <= 0:
        return 0
    return min(9, int(e * 2.2))
