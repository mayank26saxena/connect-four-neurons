# their stones (O) and my stones (X) by column, averaged over all stones, plus a bonus for the column of their last move
WO = [0.3, -0.6, 1.0, 0.6, -0.3, -0.1, 0.3]
WX = [-0.6, 0.4, 0.0, 0.0, -0.1, -0.1, 0.6]
WL = [0.3, -0.6, 0.3, 0.5, -0.2, -0.3, -0.3]

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
    return s / b.ply + WL[b.last_col]

def fires(b):
    s = score(b)
    return max(0.0, min(1.0, (s - 0.2) / 1.0))

def level(b):
    s = score(b)
    return max(0, min(9, int((s - 0.3) * 10)))
