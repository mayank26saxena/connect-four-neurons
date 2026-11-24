def fires(b):
    return b.heights[1] == 0 and max(b.heights) <= 4 and b.ply <= 14

def level(b):
    if max(b.heights) >= 6:
        return 0
    s = 7 - max(0, b.ply - 4) // 3 - max(0, max(b.heights) - 3) * 2
    if b.heights[1] == 0:
        s += 2
    return max(0, min(9, s))
