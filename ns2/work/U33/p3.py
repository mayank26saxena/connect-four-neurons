WM = [-0.05, 0.3, -0.02, 0.24, 0.11, -0.37, -0.17]
WT = [0.0, -0.02, 0.2, 0.0, -0.03, -0.17, 0.0]
WL = [0.8, 0.6, 0.35, 0.8, 0.6, -0.5, -0.2]

def score(b):
    n = 0
    t = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 0 or (r == b.last_row and c == b.last_col):
                continue
            n += 1
            t += WM[c] if v == 1 else WT[c]
    s = WL[b.last_col] + 10.0 * t / max(n, 1)
    if b.last_row == 5:
        s += 0.4
    return s

def fires(b):
    if b.last_col is None or b.ply < 4:
        return False
    return score(b) >= 1.5

def level(b):
    if b.last_col is None or b.ply < 4:
        return 0
    return max(0, min(9, int((score(b) - 0.5) * 6)))
