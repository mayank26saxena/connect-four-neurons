WME = [-0.2, 0.0, -0.05, -0.12, -0.55, -0.3, -0.1]
WTH = [-0.15, -0.25, -0.12, -0.05, -0.05, -0.1, 0.1]
LAST = [-0.47, -0.72, -1.1, -0.37, -0.3, -0.37, 0.0]

def score_(b):
    s = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                s += WME[c]
            elif v == 2:
                s += WTH[c]
    a = 1.3 + 8.0 * s / max(b.ply, 1)
    lc = b.last_col
    if lc is not None:
        a += LAST[lc]
        if lc in (4, 5) and b.last_row is not None and b.last_row >= 1:
            a -= 0.6
    if b.ply > 8:
        a -= 0.08 * (b.ply - 8)
    return a

def fires(b):
    return score_(b) > 0.6

def level(b):
    a = score_(b)
    if a <= 0.0:
        return 0
    return max(0, min(9, int(a / 0.14)))
