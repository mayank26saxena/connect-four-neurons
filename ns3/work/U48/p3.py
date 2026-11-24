MINE0 = [0.1, 0.5, 0.3, 0.45, 0.2, 0.0, -0.3]
THEIRS0 = [0.1, -0.2, 0.2, -0.2, 0.3, -0.3, 0.0]

def raw(b):
    s = 0.0
    for c in range(7):
        v = b.grid[0][c]
        if v == 1:
            s += MINE0[c]
        elif v == 2:
            s += THEIRS0[c]
    c = b.last_col
    r = b.last_row
    if c == 4 and r == 5:
        s += 0.9
    elif c == 4 and r == 0:
        s += 0.4
    elif c == 2 and r == 0:
        s += 0.3
    elif c == 4 and r == 4:
        s += 0.4
    elif c == 2 and r == 1:
        s += 0.3
    if b.heights[0] >= 3:
        s += 0.3 + 0.1 * b.heights[0]
    return s

def fires(b):
    return raw(b) >= 1.0

def level(b):
    x = raw(b)
    return max(0, min(9, int((x - 0.2) * 6)))
