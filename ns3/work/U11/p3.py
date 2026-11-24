def early_points(b):
    empty = sum(1 for h in b.heights if h == 0)
    full = sum(1 for h in b.heights if h == 6)
    s = 0
    if b.ply <= 8:
        s += 3
    elif b.ply <= 14:
        s += 2
    elif b.ply <= 20:
        s += 1
    s += min(empty, 3)
    s -= 2 * full
    if b.heights[3] <= 2:
        s += 1
    return s

def fires(b):
    return early_points(b) >= 7

def level(b):
    return max(0, min(9, early_points(b) + 1))
