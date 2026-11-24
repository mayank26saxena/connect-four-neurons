def fires(b):
    return b.heights[4] in (1, 2) and b.heights[3] >= 4

def level(b):
    if not fires(b):
        return 0
    return 5 + (2 if b.heights[3] == 6 else 0) + (2 if b.last_col == 4 else 0)
