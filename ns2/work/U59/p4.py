def fires(b):
    h = b.heights
    return h[6] == 0 and h[0] <= 1 and h[4] < h[3] + 1 and len(b.my_wins) == 0

def level(b):
    h = b.heights
    s = (h[6] == 0) + (h[0] <= 1) + (h[4] <= h[3]) + (len(b.my_wins) == 0) + (h[2] > 0 and h[5] > 0)
    return [0, 0, 1, 2, 4, 7][s]
