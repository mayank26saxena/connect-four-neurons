def score(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 1: s += 2
    if g[0][1] == 2: s += 1
    if g[0][1] == 1: s -= 1.5
    if g[0][2] == 1: s += 0.5
    if g[0][5] == 2: s += 1
    if g[0][6] == 2: s += 1
    if g[0][4] == 1: s -= 1.5
    if g[0][4] == 2: s -= 1
    if g[1][0] == 2: s -= 0.7
    return s

def fires(b):
    s = score(b)
    if b.me_first:
        return s >= 5.5
    return s >= 3

def level(b):
    s = score(b)
    if b.me_first:
        s = s - 2.5
    v = int(round((s - 2) * 2))
    return max(0, min(9, v))
