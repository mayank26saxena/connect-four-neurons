def fires(b):
    return 3 <= b.ply <= 10 and b.heights[3] == 0

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.ply <= 7:
        s += 2
    if b.last_row is not None and b.last_row >= 1:
        s += 2
    if b.heights[4] == 0 or b.heights[2] == 0:
        s += 1
    return min(9, s)
