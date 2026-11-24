def strength(b):
    g = b.grid
    s = 0
    if g[3][5] == 2 and g[2][5] == 1:
        s = 6
        if g[1][5] == 1:
            s = 8
            if g[0][5] == 1:
                s = 9
    if g[3][3] == 2 and g[2][3] == 1 and g[1][3] == 1:
        s = max(s, 6)
    if s > 0:
        # crowded boards and opponent stones in column 2 weaken it
        their2 = sum(1 for r in range(6) if g[r][2] == 2)
        s -= their2
        if b.ply > 20:
            s -= 2
        if b.ply > 28:
            s -= 2
    return max(0, min(9, s))

def fires(b):
    return strength(b) >= 7

def level(b):
    return strength(b)
