def fires(b):
    return 3 <= b.ply <= 10 and b.heights[3] == 0

def level(b):
    if b.ply < 3:
        return 0
    s = 0
    if b.heights[3] == 0:
        s += 4
    elif b.heights[3] == 1:
        s += 2
    if b.ply <= 10:
        s += 3
    elif b.ply <= 16:
        s += 1
    if b.last_row is not None and b.last_row >= 1:
        s += 1
    return min(9, s)
