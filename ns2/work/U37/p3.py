WM = [-2.5, 1.0, 0.4, 1.0, 0.0, 0.25, 0.05]   # per stone of mine, by column
WT = [0.3, -0.5, -0.2, 1.2, 0.0, 0.2, 0.1]    # per stone of theirs, by column

def score(b):
    s = 0.0
    for c in range(7):
        for r in range(b.heights[c]):
            s += WM[c] if b.grid[r][c] == 1 else WT[c]
    s = s / max(b.ply, 1)
    if b.last_col == 0:
        s += 0.15
    return s

def fires(b):
    return score(b) >= 0.62

def level(b):
    s = score(b)
    if s < 0.4:
        return 0
    return max(0, min(9, int((s - 0.4) * 11)))
