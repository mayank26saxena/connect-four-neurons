def score_(b):
    lc = b.last_col
    if lc is None:
        return -9
    w = {4: 3, 2: 2, 6: 1, 1: 0, 3: -1, 0: -2, 5: -2}
    s = w[lc]
    g = b.grid
    if g[0][2] == 2:
        s += 1
    if g[0][4] == 2:
        s += 1
    for c in (0, 5):
        for r in range(6):
            if g[r][c] == 2:
                s -= 1
    if b.ply > 14:
        s -= 1
    return s

def fires(b):
    return score_(b) >= 4

def level(b):
    s = score_(b)
    if s < 1:
        return 0
    return min(9, (s - 1) * 2)
