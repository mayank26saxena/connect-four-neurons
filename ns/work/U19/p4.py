PX = [(0, 1), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (2, 3), (2, 4), (2, 5)]

def tscore(b):
    g = b.grid
    s = 0.0
    # opponent stone on top of / in column 5 low
    if g[0][5] == 1:
        s += 1.5
        if g[1][5] == 2:
            s += 2.0
    elif g[1][5] == 2:
        s += 1.5
    # my (0,4) stone hemmed in from the left
    if g[0][4] == 1:
        s += 1.0
        s += 1.5 * (g[0][3] == 2) + 1.0 * (g[0][2] == 2) + 1.0 * (g[1][3] == 2) + 0.5 * (g[1][2] == 2)
    elif g[0][3] == 1:
        # my (0,3) stone flanked on both sides
        s += 1.0 + 1.0 * (g[0][2] == 2) + 1.5 * (g[0][4] == 2)
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
    return max(0, min(9, int(round(1.5 * (s - 2.5)))))
