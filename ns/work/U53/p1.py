def fires(b):
    return b.heights[2] == 2

def level(b):
    h = b.heights[2]
    if h == 2:
        return 7
    if h == 3 or h == 1:
        return 3
    return 0
