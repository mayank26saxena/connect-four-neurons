def fires(b):
    return b.heights[1] == 1

def level(b):
    if b.heights[1] != 1:
        return 0
    return min(9, 2 + b.ply // 4)
