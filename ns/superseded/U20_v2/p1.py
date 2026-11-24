def fires(b):
    h1 = b.heights[1]
    return h1 in (1, 2, 4, 5) and b.heights[0] < h1 and b.ply <= 28

def level(b):
    return 5 if fires(b) else 0
