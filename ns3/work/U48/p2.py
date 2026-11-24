def fires(b):
    return level(b) >= 5

def level(b):
    c = b.last_col
    r = b.last_row
    if c is None:
        return 0
    s = 0
    if c == 4 and r == 5:
        s = 6
    elif c == 4 and r == 0:
        s = 5
    elif c == 2 and r == 0:
        s = 5
    elif c == 0 and r == 0:
        s = 3
    elif c == 2 and r == 1:
        s = 3
    elif c == 4 and r == 4:
        s = 3
    elif c == 3 and r <= 2:
        s = 2
    # my stone right next to the new stone on the left side (3 -> 4) helps
    if c == 4 and b.grid[r][3] == 1:
        s += 2
    if b.heights[0] >= 3 and b.ply <= 12:
        s += 2
    return min(9, s)
