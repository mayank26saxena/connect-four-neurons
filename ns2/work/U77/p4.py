MINE_W = [2.0, -1.5, 0.7, 0.0, -2.0, -0.5, 0.0]
THEIR_W = [-0.8, 0.8, -0.3, 0.0, -1.0, 1.2, 1.0]

def est(b):
    g = b.grid
    s = 0.0
    for c in range(7):
        col = [g[r][c] for r in range(6)]
        if 1 in col:
            s += MINE_W[c]
        if 2 in col:
            s += THEIR_W[c]
    a = (s - 1.6) * 0.65 - 0.2 * (b.ply - 5)
    if b.me_first:
        a = a * 0.2
    return a

def fires(b):
    return est(b) > 0.33

def level(b):
    a = est(b)
    if a <= 0.1:
        return 0
    return max(1, min(9, int(round(a * 3))))
