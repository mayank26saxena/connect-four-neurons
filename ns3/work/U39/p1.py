def fires(b):
    return b.last_col == 1 and b.heights[1] == 1

def level(b):
    if not fires(b):
        return 0
    if b.ply <= 4:
        return 9
    if b.ply <= 6:
        return 6
    if b.ply <= 12:
        return 5
    return 4
