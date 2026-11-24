def deep_center(b):
    return any(c in (2, 3, 4) and b.heights[c] <= 3 for c in b.legal)

def fires(b):
    if b.ply < 28 or len(b.legal) > 3:
        return False
    return b.last_row == 5 and deep_center(b)

def level(b):
    if b.ply < 28 or len(b.legal) > 3:
        return 0
    s = 0
    if b.last_row == 5:
        s += 3
    if deep_center(b):
        s += 3
    s += 3 - len(b.legal) + 1
    return min(9, s)
