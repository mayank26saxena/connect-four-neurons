WM = [-0.5, 1.0, -0.5, 1.0, -1.0, -0.5, -1.0]
WT = [0.3, -0.3, -0.3, 0.0, -0.4, -0.3, -0.3]
WL = [0.2, 0.0, -0.2, 0.2, 0.5, -1.2, -0.4]

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
    return WL[b.last_col] + 3.0 * t / max(n, 1)

def late(b):
    return b.ply >= 20 and b.last_row == 5 and b.last_col in (3, 6)

def fires(b):
    if b.last_col is None or b.ply < 4:
        return False
    if b.ply <= 10:
        return score(b) >= 0.9
    return late(b)

def level(b):
    if b.last_col is None or b.ply < 4:
        return 0
    if b.ply <= 10:
        return max(0, min(9, int((score(b) + 0.3) * 3)))
    if late(b):
        return 5
    return 2 if b.last_row == 5 else 1
