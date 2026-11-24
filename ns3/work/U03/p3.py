def score_(b):
    g = b.grid
    s = 0
    if g[2][3] == 1:
        s += 2
    if g[1][3] == 2:
        s += 1
    s += min(2, sum(1 for c in (0, 1, 2) if g[0][c] == 2))
    s -= sum(1 for c in (0, 1) for r in (0, 1) if g[r][c] == 1)
    if g[0][4] == 2:
        s -= 2
    s -= b.heights[4]
    if b.ply <= 10:
        s += 1
    if b.ply >= 22:
        s -= 1
    return s

def fires(b):
    return score_(b) >= 4

def level(b):
    return max(0, min(9, 2 * score_(b) - 1))
