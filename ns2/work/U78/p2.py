WO = [1.0, -1.5, 1.0, 0.8, -0.3, -0.3, 0.0]
WX = [-1.5, 0.0, -0.8, -0.2, 0.4, -0.3, 0.5]
WL = [1.5, -1.5, 0.8, 1.5, 0.0, -1.0, -1.0]

def score(b):
    if b.last_col is None or b.ply == 0:
        return -9.0
    s = 0.0
    for c in range(7):
        for r in range(b.heights[c]):
            v = b.grid[r][c]
            if v == 2:
                s += WO[c]
            elif v == 1:
                s += WX[c]
    return s / b.ply * 4 + WL[b.last_col]

def fires(b):
    return score(b) > 2.6

def level(b):
    s = score(b)
    return max(0, min(9, int((s - 1.0) * 3)))
