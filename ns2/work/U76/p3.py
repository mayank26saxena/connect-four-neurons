def fires(b):
    g = b.grid
    if b.heights[2] > 1:
        return False
    return g[4][3] == 1 or g[2][1] == 1

def level(b):
    g = b.grid
    s = 0
    if g[4][3] == 1:
        s += 3
    if g[2][1] == 1:
        s += 3
    if s == 0:
        return 0
    h = b.heights[2]
    if h == 0:
        s += 2
    elif h == 1:
        s += 1
    else:
        s = s // 3
    return min(s, 9)
