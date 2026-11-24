def depth(b):
    h = b.heights
    return min(h[1], h[3]) - h[2]

def fires(b):
    return depth(b) >= 3

def level(b):
    d = depth(b)
    if d <= 1:
        return 0
    return min(9, (d - 1) * 2)
