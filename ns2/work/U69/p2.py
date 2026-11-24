WME = [-0.25, 0.0, 0.0, -0.15, -0.6, -0.1, -0.05]
WTH = [-0.05, -0.2, -0.07, -0.16, 0.0, 0.05, 0.24]
LAST = [-0.47, -0.72, -1.1, -0.37, -0.47, -0.37, 0.0]

def score_(b):
    s = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                s += WME[c]
            elif v == 2:
                s += WTH[c]
    a = 1.14 + 8.0 * s / max(b.ply, 1)
    if b.last_col is not None:
        a += LAST[b.last_col]
    if b.ply > 8:
        a -= 0.07 * (b.ply - 8)
    return a

def fires(b):
    return score_(b) > 0.589

def level(b):
    a = score_(b)
    if a <= 0.2:
        return 0
    return max(0, min(9, int((a - 0.2) / 0.12)))
