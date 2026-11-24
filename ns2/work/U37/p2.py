WM = [-2.5, 1.0, 0.4, 1.0, 0.0, 0.25, 0.0]   # weight per stone of mine in each column
WT = [1.2, 0.0, 0.3, 1.3, 0.5, 0.6, 0.6]     # weight per stone of theirs in each column

def score(b):
    s = 0.0
    for c in range(7):
        for r in range(b.heights[c]):
            s += WM[c] if b.grid[r][c] == 1 else WT[c]
    return s / max(b.ply, 1)

def fires(b):
    return score(b) >= 0.72

def level(b):
    s = score(b)
    if s < 0.5:
        return 0
    return max(0, min(9, int((s - 0.5) * 12)))
