def fires(b):
    return b.heights[2] == 0 and 6 <= b.ply <= 20

def level(b):
    if b.heights[2] != 0:
        return 0
    if b.ply < 6 or b.ply > 22:
        return 1
    return 5
