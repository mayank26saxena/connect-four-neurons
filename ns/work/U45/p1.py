def fires(b):
    # column 2 empty, game past the opening, centre columns occupied
    return b.heights[2] == 0 and 6 <= b.ply <= 20 and b.heights[3] + b.heights[4] >= 3

def level(b):
    if not fires(b):
        return 0
    s = 5
    if b.heights[1] == 0:
        s += 2
    if b.heights[0] > 0:
        s += 1
    return min(9, s)
