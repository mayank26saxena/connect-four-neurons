def fires(b):
    return b.heights[6] == 3 and b.ply % 2 == 1 and b.ply >= 13

def level(b):
    if b.heights[6] != 3:
        return 0
    if b.ply < 13:
        return 1
    if b.ply % 2 == 0:
        return 3
    return min(9, 5 + (b.ply - 13) // 5)
