def score_of(b):
    g = b.grid
    s = 0.0
    # alternating stripe in the centre: theirs on rows 1 and 3, mine on rows 2 and 4
    wcol = {3: 1.0, 2: 0.5}
    for c in (2, 3):
        w = wcol[c]
        for r in (1, 2, 3, 4):
            want = 2 if r % 2 == 1 else 1
            v = g[r][c]
            if v == want:
                s += w * (3 if (c == 3 and r <= 2) else 1.5)
            elif v != 0:
                s -= w * 2
    # bottom-row stones of theirs beside the centre
    if g[0][2] == 2:
        s += 1.5
    elif g[0][2] == 0:
        s -= 1.5
    if g[0][5] == 2:
        s += 1
    # column 4: (2,4) must be empty, their stone at (1,4) helps, mine hurts
    if g[2][4] == 2:
        s -= 5
    elif g[2][4] == 1:
        s -= 2.5
    if g[1][4] == 2:
        s += 1
    elif g[1][4] == 1:
        s -= 1.5
    if g[1][5] == 2:
        s += 1
    elif g[1][5] == 1:
        s -= 1.5
    if g[1][6] == 1:
        s -= 1
    # outer columns filled above the bottom row hurt
    for c in (0, 6):
        for r in range(1, 6):
            if g[r][c] != 0:
                s -= 0.4
    return s

def fires(b):
    return score_of(b) >= 7

def level(b):
    s = score_of(b)
    if s < 3:
        return 0
    return max(0, min(9, int((s - 3) * 0.9)))
