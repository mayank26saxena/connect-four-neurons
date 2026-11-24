def fires(b):
    return level(b) >= 5

def level(b):
    h = b.heights
    if h[4] == 6 and h[5] == 6:
        return 0
    s = 0
    s += 3 if h[1] == 6 else (1 if h[1] == 5 else 0)
    s += 2 if h[0] == 6 else (1 if h[0] == 5 else 0)
    s += 1 if h[2] == 6 else 0
    s += 1 if h[3] == 6 else 0
    s += 1 if h[6] == 6 else 0
    if h[4] == 6 or h[5] == 6:
        s -= 2
    return max(0, min(9, s))
