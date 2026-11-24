def fires(b):
    g = b.grid
    return g[1][1] == 1 and g[1][3] == 2 and g[1][2] == 0

def level(b):
    g = b.grid
    s = 0
    if g[1][1] == 1: s += 2
    if g[1][3] == 2: s += 2
    if g[1][2] == 0: s += 1
    if g[0][3] == 1: s += 1
    if g[0][2] == 1: s += 1
    if b.me_first: s += 1
    if b.ply <= 10: s += 1
    return min(9, s)
