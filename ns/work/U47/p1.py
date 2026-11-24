def fires(b):
    return b.last_col == 1 and b.heights[1] == 3

def level(b):
    if fires(b):
        return 9
    if b.heights[1] == 3:
        return 3
    return 0
