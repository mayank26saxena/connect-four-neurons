def score_of(b):
    g = b.grid
    s = 0.0
    if g[1][3] == 2:
        s += 3
    elif g[1][3] == 1:
        s -= 1
    if g[2][3] == 1:
        s += 2.5
    elif g[2][3] == 2:
        s -= 2
    if g[0][3] == 1:
        s += 0.5
    if g[0][2] == 2:
        s += 1.5
    elif g[0][2] == 0:
        s -= 2
    if g[0][5] == 2:
        s += 1
    elif g[0][5] == 0:
        s -= 0.5
    if g[0][4] == 1:
        s += 1
    if g[1][5] == 2:
        s += 1
    elif g[1][5] == 1:
        s -= 1.5
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
    if g[1][4] == 2:
        s += 1.5
    elif g[1][4] == 1:
        s -= 1.5
    if g[1][6] == 1:
        s -= 1
    if g[2][4] == 2:
        s -= 5
    elif g[2][4] == 1:
        s -= 2.5
    for r in range(3, 6):
        if g[r][4] != 0:
            s -= 1
    for c in (0, 6):
        for r in range(1, 6):
            if g[r][c] != 0:
                s -= 0.5
    if b.ply > 14:
        s -= 0.15 * (b.ply - 14)
    return s

def fires(b):
    # graded: 0.5 at score 7, saturating at 0 and 1
    return max(0.0, min(1.0, 0.5 + (score_of(b) - 7) / 8))

def level(b):
    s = score_of(b)
    if s < 3:
        return 0
    return max(0, min(9, int(s - 3)))
