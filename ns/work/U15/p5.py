def raw(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 2:
        s += 3
    if g[1][0] == 2:
        s += 1.5
    if g[0][6] == 2:
        s += 2.5
    if g[1][6] == 2:
        s += 1
    if g[0][1] == 2:
        s += 1
    if g[1][3] == 1:
        s += 2
    elif g[1][3] == 2:
        s -= 2
    h = b.heights[3]
    if h >= 2 and g[h - 1][3] == 2:
        s -= 1.5
    if b.me_first:
        s += 1.5 if b.ply <= 10 else 0.5
    if b.ply <= 8:
        s += 1
    return s

def fires(b):
    return raw(b) >= 6.5

def level(b):
    return max(0, min(9, int(raw(b) * 1.2) - 3))
