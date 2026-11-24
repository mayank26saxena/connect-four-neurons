def score_(b):
    g = b.grid
    s = 0
    if g[1][1] == 1: s += 2
    if g[1][3] == 2: s += 2
    if g[0][3] == 1: s += 1
    if g[0][2] == 1: s += 1
    if g[1][2] == 0: s += 1
    if b.me_first: s += 1
    if b.ply <= 12: s += 1
    if b.heights[0] == 0: s += 1
    return s

def fires(b):
    return score_(b) >= 8

def level(b):
    s = score_(b)
    return max(0, min(9, s))
