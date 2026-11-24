def score(b):
    g = b.grid
    s = 0.0
    if b.heights[5] == 0:
        s += 1.0
    if b.heights[1] == 0:
        s += 0.5
    n6 = 0
    mine6 = False
    for r in range(b.heights[6]):
        if g[r][6] == 2:
            n6 += 1
        else:
            mine6 = True
    if mine6:
        s -= 1.0
    else:
        s += 0.8 * n6
    if g[0][3] == 1:
        s += 1.0
    if g[1][3] == 1:
        s += 0.7
    if g[1][2] == 2:
        s += 0.5
    if g[1][4] == 1:
        s += 0.4
    if g[0][3] == 2:
        s -= 0.5
    if b.ply > 14:
        s -= 1.0
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 2.5:
        return 0
    return max(0, min(9, int(round((s - 2.5) * 2.5))))
