def fires(b):
    return b.heights[2] == 0 and b.heights[1] <= 1 and 6 <= b.ply <= 20

def level(b):
    if b.heights[2] != 0:
        return 0
    s = 2
    if 6 <= b.ply <= 20:
        s += 2
    if b.heights[1] == 0:
        s += 3
    elif b.heights[1] == 1:
        s += 1
    return min(s, 9)
