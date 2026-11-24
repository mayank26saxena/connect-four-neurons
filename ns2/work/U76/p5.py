def score_cells(b):
    g = b.grid
    h2 = b.heights[2]
    if h2 >= 3:
        return 0
    s = 0
    if g[4][3] == 1:
        s += 3
    if g[2][1] == 1:
        s += 3
    if g[2][3] == 2:
        s += 1
    if g[3][1] == 2:
        s += 1
    if g[3][3] == 2:
        s += 1
    if h2 == 0:
        s += 1
    elif h2 == 2:
        s -= 1
    return s

def fires(b):
    return score_cells(b) >= 5

def level(b):
    s = score_cells(b)
    if s <= 2:
        return 0
    return min(9, (s - 2) * 2)
