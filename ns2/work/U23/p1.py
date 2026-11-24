def fires(b):
    return b.heights[5] == 6 and b.ply >= 30

def level(b):
    if b.heights[5] != 6:
        return 0
    v = (b.ply - 22) // 2
    return max(0, min(9, v))
