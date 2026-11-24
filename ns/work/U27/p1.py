def fires(b):
    return b.heights[0] >= 5 and b.last_col == 0

def level(b):
    h = b.heights[0]
    if b.last_col == 0 and h >= 5:
        return 9 if h == 6 else 7
    if h == 6:
        return 4
    if h == 5:
        return 3
    return 0
