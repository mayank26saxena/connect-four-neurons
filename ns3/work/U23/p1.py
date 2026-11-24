def fires(b):
    return b.last_col == 1 and b.heights[1] <= 2 and b.ply < 20

def level(b):
    if b.last_col != 1 or b.ply >= 20:
        return 0
    if b.heights[1] == 1:
        return 7 if b.ply < 15 else 5
    if b.heights[1] == 2:
        return 4
    return 1
