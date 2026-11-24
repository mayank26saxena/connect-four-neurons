def top(b, c):
    h = b.heights[c]
    return b.grid[h - 1][c] if h > 0 else 0

def pts(b):
    if b.last_col is None or b.ply < 3:
        return 0
    s = 0
    g = b.grid
    for c in (3, 4):
        if b.heights[c] >= 2 and g[1][c] == 1 and g[0][c] == 2:
            s += 2          # my stone sitting on theirs in row 1 of a centre column
        elif b.heights[c] == 2:
            s += 0.5
        if b.heights[c] >= 1 and top(b, c) == 2 and b.last_col == c:
            s -= 1.5        # they just covered the centre column
    if b.heights[6] >= 2 and top(b, 6) == 2:
        s += 1.5
        if b.heights[6] >= 3 and g[b.heights[6] - 2][6] == 2:
            s += 1
    if b.last_col in (0, 6):
        s += 1
    return s

def fires(b):
    return pts(b) >= 3

def level(b):
    return max(0, min(9, int(pts(b) * 1.5)))
