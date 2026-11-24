def raw(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 2:
        s += 4
        if g[0][1] == 2:
            s += 1
    if g[0][6] == 2:
        s += 2.5
    if b.me_first:
        s += 1.5
    if b.ply <= 8:
        s += 1.5
    elif b.ply <= 14:
        s += 0.5
    if g[0][3] == 1:
        s += 1
        if g[1][3] == 2:
            s -= 3
    if g[0][3] == 2:
        s -= 2
    return s

def fires(b):
    return raw(b) >= 7.5

def level(b):
    v = int(raw(b)) - 2
    return max(0, min(9, v))
