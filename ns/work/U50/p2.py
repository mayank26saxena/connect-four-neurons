LASTW = {0: 1.3, 1: -2.5, 2: -0.7, 3: 1.2, 4: 0.6, 5: 0.7, 6: 1.2}

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
    if b.ply % 2 == 0:
        s += LASTW[b.last_col]
    else:
        s += 0.0
    s -= 0.15 * (b.ply - 2)
    if mine1:
        s = min(s, 0.3)
    return s

def fires(b):
    return score(b) > 0.75

def level(b):
    s = score(b)
    if s <= 0.3:
        return 0
    return max(0, min(9, int(round((s - 0.3) * 3))))
