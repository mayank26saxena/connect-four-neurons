def fires(b):
    return max(b.heights) <= 4 and b.ply <= 16

def level(b):
    if max(b.heights) == 6:
        return 0
    s = 9 - max(0, b.ply - 4) // 2 - max(0, max(b.heights) - 3) * 2
    return max(0, min(9, s))
