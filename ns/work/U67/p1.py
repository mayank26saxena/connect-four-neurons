def fires(b):
    return b.heights[1] == 0 and b.ply >= 5

def level(b):
    if b.heights[1] != 0:
        return 0
    return min(9, 2 + b.ply // 4)
