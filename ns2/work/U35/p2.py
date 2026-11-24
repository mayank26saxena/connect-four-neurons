WME = [0.2, 0.0, 0.1, 0.0, 0.42, -0.23, 0.62]
WTH = [-0.35, 0.0, -0.24, -0.33, 0.0, 0.0, 0.09]
WLAST = [0.0, 0.2, 0.1, 0.05, 0.4, 0.75, 0.55]

def score(b):
    if b.last_col is None:
        return -9.0
    s = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                s += WME[c]
            elif v == 2 and not (r == b.last_row and c == b.last_col):
                s += WTH[c]
    n = max(1, b.ply - 1)
    return -0.15 + WLAST[b.last_col] - 0.3 * b.last_row + 3.0 * s / n - 0.03 * (b.ply - 4)

def fires(b):
    return score(b) > 0.632

def level(b):
    s = score(b)
    if s <= 0.3:
        return 0
    return max(0, min(9, int((s - 0.3) / 0.12)))
