def fires(b):
    lr = [b.landing(c) for c in range(7)]
    if 3 in lr:
        return False
    if b.heights[6] > 2:
        return False
    return 2 in lr

def level(b):
    if not fires(b):
        return 0
    lr = [b.landing(c) for c in range(7)]
    return min(9, 3 + 2 * lr.count(2))
