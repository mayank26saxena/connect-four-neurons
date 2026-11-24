def score(b):
    p = b.ply
    c = b.last_col
    r = b.last_row
    if c is None or r is None:
        return -1.0
    odd = p % 2 == 1
    if not odd:
        if p <= 12:
            s = 0.65
        elif p <= 14:
            s = 0.5
        elif p <= 22:
            s = 0.2
        else:
            s = 0.0
        if p <= 14:
            if c == 0:
                s -= 0.6
            elif c == 2:
                s -= 0.3
            elif c == 6 and p <= 6 and r == 0:
                s -= 0.4
            elif c in (3, 4):
                s += 0.1
            if r >= 3:
                s -= 0.3
        return s
    if p == 5:
        s = 0.6
        if c in (0, 2):
            s -= 0.4
        return s
    if p < 23:
        s = 0.1
        if c == 0 and r >= 3:
            s += 0.3
        return s
    s = 0.45 if p == 23 else 0.6
    if p >= 37:
        s = 0.2
    if c == 0:
        s += [-0.5, -0.5, -0.1, 0.1, 0.2, 0.35][r]
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
    if b.heights[0] == 6 and c != 0:
        s += 0.1
    return s

def fires(b):
    return score(b) >= 0.8

def level(b):
    s = score(b)
    return max(0, min(9, int(round((s - 0.2) * 9))))
