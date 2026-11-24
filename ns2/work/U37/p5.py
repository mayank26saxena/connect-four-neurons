WM = [-2.5, 1.0, 0.5, 0.9, 0.0, 0.4, 0.0]   # per stone of mine, by column
WT = [1.2, -0.3, 0.0, 1.0, 0.4, 0.5, 0.5]    # per stone of theirs, by column

def score(b):
    s = 0.0
    for c in range(7):
        for r in range(b.heights[c]):
            s += WM[c] if b.grid[r][c] == 1 else WT[c]
    s = s / max(b.ply, 1)
    if b.last_col == 0:
        s += 0.1
    return s

def fires(b):
    # continuous: 0.5 at the threshold 0.66
    return max(0.0, min(1.0, 0.5 + (score(b) - 0.66) * 2.0))

def level(b):
    s = score(b)
    if s < 0.5:
        return 0
    return max(0, min(9, int((s - 0.5) * 12)))
