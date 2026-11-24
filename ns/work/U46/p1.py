def share(b):
    if b.ply == 0:
        return 0.0
    h = b.heights
    return (h[2] - 0.5 * (h[0] + h[1])) / b.ply

def fires(b):
    if b.ply == 1:
        return b.heights[2] == 1
    return b.heights[2] >= 3 and share(b) >= 0.3

def level(b):
    if not fires(b):
        return 0
    s = share(b) * b.heights[2]
    return max(1, min(9, int(s * 3)))
