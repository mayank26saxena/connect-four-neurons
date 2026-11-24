LASTW = {0: 1.3, 1: -2.5, 2: -0.7, 3: 1.2, 4: 0.6, 5: 0.7, 6: 1.2}
ODDW = {0: 0.0, 1: -0.6, 2: -0.6, 3: -0.3, 4: -0.8, 5: 0.0, 6: -0.4}

def score(b):
    if b.ply < 2 or b.last_col is None:
        return -9.0
    s = 0.0
    mine1 = False
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 0:
                continue
            if c == 1:
                if v == 1:
                    mine1 = True
                s -= 0.8 if v == 1 else 1.0
            elif c == 2 and v == 2:
                s -= 0.4
            elif c == 4:
                s -= 0.15
            elif c == 0 or c == 5:
                s += 0.3
    if b.ply <= 5:
        for c in (0, 5):
            if b.heights[c] >= 3:
                s += 0.6
    if b.ply % 2 == 0:
        s += LASTW[b.last_col]
    else:
        s += ODDW[b.last_col]
    s -= 0.15 * (b.ply - 2)
    if b.ply > 6:
        s -= 0.25 * (b.ply - 6)
    if mine1:
        s = min(s, 0.3)
    return s

def fires(b):
    return score(b) > 0.7

def level(b):
    s = score(b)
    if s <= 0.3:
        return 0
    return max(0, min(9, int(round((s - 0.3) * 3))))
