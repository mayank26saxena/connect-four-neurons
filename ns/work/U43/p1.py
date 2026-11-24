def fires(b):
    return b.heights[6] == 3 and b.last_col != 6 and b.ply >= 14

def level(b):
    if b.heights[6] != 3:
        return 0
    if b.last_col == 6:
        return 1
    if b.ply < 14:
        return 2
    return min(9, 4 + (b.ply - 14) // 4)
