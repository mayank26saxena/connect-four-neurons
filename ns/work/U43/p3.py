def fires(b):
    return b.heights[6] == 3 and b.heights[3] + b.heights[4] >= 9

def level(b):
    if b.heights[6] != 3:
        return 0
    m = b.heights[3] + b.heights[4]
    return max(1, min(9, m - 3))
