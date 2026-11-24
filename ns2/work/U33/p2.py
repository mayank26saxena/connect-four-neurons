WME = [0.25, 1.0, 0.4, 0.9, 0.0, 0.6, 0.0]
WTH = [0.5, 0.15, 0.1, 0.3, 0.0, 0.25, 0.15]
WLAST = [0.65, 0.45, 0.25, 0.7, 1.0, 0.0, 0.1]

def early_score(b):
    s = WLAST[b.last_col]
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                s += WME[c]
            elif v == 2 and not (r == b.last_row and c == b.last_col):
                s += WTH[c]
    return s

def late_hit(b):
    if b.last_row == 5 and b.last_col in (0, 3, 6):
        return True
    return b.last_col == 3 and b.last_row == 4

def fires(b):
    if b.last_col is None or b.ply < 4:
        return False
    if b.ply <= 6:
        return early_score(b) >= 1.9 + 0.3 * (b.ply - 4)
    return late_hit(b)

def level(b):
    if b.last_col is None or b.ply < 4:
        return 0
    if b.ply <= 6:
        s = early_score(b) - 0.3 * (b.ply - 4)
        return max(0, min(9, int((s - 1.0) * 4)))
    if late_hit(b):
        return 6 if b.last_row == 5 else 4
    return 1
