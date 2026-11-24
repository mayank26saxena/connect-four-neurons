MINE0 = [0.0, 0.55, 0.35, 0.5, 0.3, 0.0, -0.4]
THEIRS0 = [0.15, -0.2, 0.2, -0.2, 0.3, -0.35, -0.1]

def early(b):
    s = -0.6
    for c in range(7):
        v = b.grid[0][c]
        if v == 1:
            s += MINE0[c]
        elif v == 2:
            s += THEIRS0[c]
    if b.last_row == 0 and b.last_col in (2, 4):
        s += 0.15
    if b.heights[0] >= 2:
        s += 0.3 * (b.heights[0] - 1)
    return s

def act(b):
    c = b.last_col
    r = b.last_row
    if b.ply <= 11:
        return early(b)
    if c == 4 and r == 5:
        return 0.7
    if c == 4 and r == 0 and b.ply >= 24:
        return 0.7
    return 0.0

def fires(b):
    return act(b) >= 0.57

def level(b):
    return max(0, min(9, int(act(b) * 7)))
