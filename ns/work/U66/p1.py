def fires(b):
    return b.last_col == 6 and 1 <= b.heights[4] <= 4

def level(b):
    if not fires(b):
        return 0
    return 6 if b.heights[4] == 2 else 4
