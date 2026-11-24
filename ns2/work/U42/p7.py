def cnt(b, c, who):
    return sum(1 for r in range(6) if b.grid[r][c] == who)

def late_score(b):
    p = b.ply
    c = b.last_col
    r = b.last_row
    s = 0.45 if p == 23 else 0.6
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

def early_ok(b):
    p = b.ply
    c = b.last_col
    if p % 2 == 1 or p > 10:
        return False
    if c not in (1, 3, 4):
        return False
    if b.last_row >= 2:
        return False
    if cnt(b, 0, 2) + cnt(b, 5, 2) + cnt(b, 6, 2) > 0:
        return False
    if cnt(b, 0, 1) > 0:
        return False
    return True

def fires(b):
    if b.last_col is None:
        return False
    p = b.ply
    if p % 2 == 1 and 23 <= p <= 35:
        return late_score(b) >= 0.8
    return early_ok(b)

def level(b):
    if b.last_col is None:
        return 0
    p = b.ply
    c = b.last_col
    r = b.last_row
    if p % 2 == 1 and 23 <= p <= 35:
        return max(0, min(9, int(round((late_score(b) - 0.2) * 9))))
    if early_ok(b):
        return 8
    if p % 2 == 0 and p <= 14:
        s = 5 if p <= 12 else 3
        if c == 0:
            s -= 4
        elif c == 2:
            s -= 2
        if r >= 3:
            s -= 2
        if c in (3, 4) and r <= 1:
            s += 1
        return max(0, min(9, s))
    if p == 5:
        return 2 if c in (0, 2) else 5
    if p % 2 == 0 and p >= 24 and c == 0 and r >= 4:
        return 4
    if p % 2 == 1 and p < 23:
        return 1
    return 2
