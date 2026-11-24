def gap(b):
    return b.heights[3] - b.heights[4]

def fires(b):
    return b.heights[4] <= 2 and gap(b) >= 2

def level(b):
    if b.heights[4] > 2:
        return 0
    g = gap(b)
    if g < 1:
        return 0
    return min(9, 2 * g)
