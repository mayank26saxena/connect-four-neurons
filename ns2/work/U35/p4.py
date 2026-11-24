def fires(b):
    return b.heights[0] == 0 and b.heights[2] == 0 and b.ply <= 18

def level(b):
    if b.heights[0] > 0 or b.heights[2] > 0:
        return 0
    return max(0, min(9, 11 - b.ply // 2))
