def fires(b):
    return b.heights[1] == 3

def level(b):
    if b.heights[1] != 3:
        return 0
    if b.last_col == 1:
        return 9
    return 5
