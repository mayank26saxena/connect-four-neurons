def s(b):
    g = b.grid
    if g[3][3] == 1 or g[2][4] == 1 or g[0][2] == 2 or g[3][4] == 2:
        return 0
    v = 0
    if g[0][2] == 1:
        v += 2
    for (r, c) in [(2, 4), (3, 3), (2, 5), (3, 2)]:
        if g[r][c] == 2:
            v += 1
    if g[3][4] == 1:
        v += 1
    if g[0][0] == 2 and g[0][1] != 1:
        v += 1
    return v

def fires(b):
    return s(b) >= 3

def level(b):
    return min(9, 2 * s(b))
