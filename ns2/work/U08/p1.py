def fires(b):
    return b.heights[0] == 6

def level(b):
    if b.heights[0] < 6:
        return 1 if b.heights[0] == 5 and b.last_col == 0 else 0
    return 9 if b.last_col == 0 else 6
