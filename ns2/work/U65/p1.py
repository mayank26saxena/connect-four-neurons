def fires(b):
    return b.ply <= 15 and b.heights[6] <= 1 and b.heights[3] >= 2 and b.heights[5] >= 1

def level(b):
    if not fires(b):
        return 0
    return 5 if b.ply <= 11 else 3
