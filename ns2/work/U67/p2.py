def level(b):
    full1 = b.heights[1] == 6
    if b.last_col == 1 and b.last_row == 5:
        if b.ply >= 18:
            return 9
        if b.ply >= 12:
            return 7
        return 5
    if full1:
        if b.ply >= 38:
            return 7
        if b.ply >= 34:
            return 6
        if b.ply >= 28:
            return 5
        return 3
    if b.last_col == 1 and b.last_row == 4:
        return 3
    return 0

def fires(b):
    return level(b) >= 6
