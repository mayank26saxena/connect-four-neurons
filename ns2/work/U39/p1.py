def fires(b):
    p1 = 1 if b.me_first else 2
    p2 = 3 - p1
    g = b.grid
    return g[1][1] == p1 and g[1][3] == p2 and g[1][2] == 0

def level(b):
    if not fires(b):
        return 0
    lv = 5
    if b.me_first:
        lv += 2
    if b.heights[2] == 1:
        lv += 2
    return lv
