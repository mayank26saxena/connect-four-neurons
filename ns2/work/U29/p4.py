def score(b):
    g = b.grid
    s = 0
    if g[4][3] == 2:
        s += 3
        if g[5][3] == 2:
            s -= 1
    if g[4][4] == 0:
        s += 1
    else:
        s -= 3
    if g[3][4] == 1:
        s -= 1
    if b.last_row == 3:
        s += 3
    elif b.last_row in (2, 4):
        s += 1
    if b.last_col in (3, 4, 5):
        s += 1
    if b.ply > 28:
        s -= 2
    return s

def fires(b):
    return score(b) >= 7

def level(b):
    return max(0, min(9, score(b)))
