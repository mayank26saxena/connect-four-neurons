def fires(b):
    return b.heights[1] == 1 and b.heights[0] + b.heights[2] >= 3

def level(b):
    if b.heights[1] != 1:
        return 0
    s = b.heights[0] + b.heights[2]
    return min(9, 1 + s)
