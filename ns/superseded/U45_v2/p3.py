def score(b):
    h = b.heights
    s = 0
    if h[2] == 0:
        s += 3
    elif h[2] == 5:
        s += 2
    if b.ply < 6 or b.ply > 22:
        s -= 3
    elif b.ply <= 14:
        s += 1
    if b.last_col is not None:
        c, r = b.last_col, b.last_row
        if c == 4 and r in (1, 2):
            s -= 2
        if c == 0 and r in (1, 2, 3):
            s += 1
        if c == 3 and r <= 1:
            s -= 1
    # their stone on (2,4)/(1,4) hurts, mine helps
    for r in (1, 2):
        if b.grid[r][4] == 2:
            s -= 1
        elif b.grid[r][4] == 1:
            s += 1
    return s

def fires(b):
    return score(b) >= 5

def level(b):
    return max(0, min(9, score(b) * 2 - 3))
