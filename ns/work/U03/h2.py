def fires(b):
    return b.ply >= 3 and b.heights[3] <= 1 and b.ply <= 14

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.heights[3] == 0:
        s += 2
    if b.ply <= 8:
        s += 2
    return s
