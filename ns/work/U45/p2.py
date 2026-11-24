def fires(b):
    # column 2 empty, my stone at the bottom of column 3, past the opening
    return b.heights[2] == 0 and b.grid[0][3] == 1 and 6 <= b.ply <= 22

def level(b):
    if not fires(b):
        return 0
    s = 5
    if b.heights[1] == 0:
        s += 2
    if b.heights[0] > 0:
        s += 1
    return min(9, s)
