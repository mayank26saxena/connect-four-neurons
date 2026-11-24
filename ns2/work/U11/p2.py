def score_of(b):
    g = b.grid
    s = 0.0
    # centre column: their stone on row 1, my stone on row 2
    if g[1][3] == 2:
        s += 3
    elif g[1][3] == 1:
        s -= 1
    if g[2][3] == 1:
        s += 2.5
    elif g[2][3] == 2:
        s -= 2
    # their stones low around the centre
    if g[0][2] == 2:
        s += 1.5
    elif g[0][2] == 0:
        s -= 2
    if g[1][5] == 2:
        s += 1
    if g[1][2] == 2:
        s += 0.5
    if g[3][2] == 2:
        s += 1
    if g[3][3] == 2:
        s += 0.5
    if g[2][2] == 1:
        s += 1
    elif g[2][2] == 2:
        s -= 1
    # my stones on row 1 to the right of centre hurt
    for c in (4, 5, 6):
        if g[1][c] == 1:
            s -= 1
    # column 4 must stay low
    for r in range(2, 6):
        if g[r][4] != 0:
            s -= 1.5
    # outer columns filled above the bottom row hurt
    for c in (0, 6):
        for r in range(1, 6):
            if g[r][c] != 0:
                s -= 0.5
    return s

def fires(b):
    return score_of(b) >= 6

def level(b):
    s = score_of(b)
    if s < 3:
        return 0
    return max(0, min(9, int(s - 2)))
