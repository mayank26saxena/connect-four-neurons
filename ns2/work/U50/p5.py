def fires(b):
    return b.last_col == 4 and b.heights[5] == 0

def level(b):
    if fires(b):
        return 9 if b.ply <= 10 else 6
    if b.last_col == 4:
        return 2
    if b.heights[5] == 0:
        return 1
    return 0
