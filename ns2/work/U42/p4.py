def cnt(b, c, who):
    return sum(1 for r in range(6) if b.grid[r][c] == who)

def score(b):
    p = b.ply
    c = b.last_col
    r = b.last_row
    if c is None or r is None:
        return -1.0
    if p % 2 == 0:
        if p > 16:
            return 0.0
        s = 0.85 - 0.03 * (p - 4)
        if c == 0:
            s -= 0.8
        elif c == 2:
            s -= 0.35
        elif c == 6 and r == 0:
            s -= 0.4
        elif c == 5:
            s -= 0.1
        s -= 0.25 * (cnt(b, 0, 2) - (1 if c == 0 else 0))
        s -= 0.15 * cnt(b, 0, 1)
        s += 0.08 * cnt(b, 6, 1)
        if r >= 3:
            s -= 0.3
        return s
    if p == 5:
        s = 0.8
        if c in (0, 2):
            s -= 0.4
        return s
    if p < 23 or p > 37:
        return 0.1
    s = 0.45 if p == 23 else 0.6
    if c == 0:
        s += [-0.5, -0.5, -0.1, 0.1, 0.25, 0.4][r]
    elif c == 6:
        s += [0.15, 0.15, -0.15, -0.15, 0.1, 0.15][r]
    elif c == 1:
        s += [-0.2, 0.0, 0.1, 0.1, -0.1, -0.5][r]
    elif c == 3:
        s += [0.0, 0.0, -0.1, 0.0, -0.6, -0.7][r]
    elif c == 4:
        s += [0.0, 0.1, 0.1, 0.1, -0.1, -0.3][r]
    else:
        s -= 0.1
    s += 0.05 * (b.heights[0] - 4)
    s -= 0.05 * (b.heights[3] - 4)
    return s

def fires(b):
    return score(b) >= 0.75

def level(b):
    s = score(b)
    return max(0, min(9, int(round((s - 0.1) * 9))))
