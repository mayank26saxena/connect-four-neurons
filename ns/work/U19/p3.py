WO = {(0, 2): 1.0, (0, 3): 1.5, (1, 2): 1.0, (1, 3): 1.0, (1, 5): 2.0}
WX = {(0, 4): 1.0, (0, 5): 1.5}
PX = [(0, 1), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (2, 3), (2, 4), (2, 5)]

def tscore(b):
    g = b.grid
    s = 0.0
    for (r, c), w in WO.items():
        if g[r][c] == 2:
            s += w
    for (r, c), w in WX.items():
        if g[r][c] == 1:
            s += w
    for (r, c) in PX:
        if g[r][c] == 1:
            s -= 1.0
    return s

def fires(b):
    return tscore(b) >= 3.5

def level(b):
    s = tscore(b)
    if s < 2.5:
        return 0
    return max(0, min(9, int(round(2 * (s - 2.5)))))
