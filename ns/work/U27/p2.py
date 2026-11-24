def fires(b):
    h0 = b.heights[0]
    h1 = b.heights[1]
    return h0 >= 5 and h1 <= 2

def level(b):
    h0 = b.heights[0]
    h1 = b.heights[1]
    v = 0
    if h0 >= 4:
        v = (h0 - 3) * 3 - h1
    return max(0, min(9, v))
