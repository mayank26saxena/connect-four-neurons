def fires(b):
    return b.last_col == 2 and b.ply <= 8 and b.heights[3] <= 1

def level(b):
    if not fires(b):
        return 0
    return 9 if b.ply <= 4 else (7 if b.ply <= 6 else 5)
