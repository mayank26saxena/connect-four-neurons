def comp(b):
    # opponent stones in cols 4-5 and my stones in col 0 push up; my stones in cols 4-6 and opponent stones in col 0 push down
    s = 0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 2:
                if c in (4, 5):
                    s += 1
                elif c == 0:
                    s -= 1
            elif v == 1:
                if c == 0:
                    s += 1
                elif c >= 4:
                    s -= 1
    return s

def fires(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return False
    k = comp(b)
    if p <= 9:
        return c <= 4 and k >= 1 and p % 2 == 1 or (c == 3 and k >= 1 and p <= 7)
    if 19 <= p <= 28:
        return c <= 3 and k >= 3
    if p >= 34:
        return c >= 5
    return False

def level(b):
    p = b.ply
    c = b.last_col
    if c is None:
        return 0
    k = comp(b)
    if p <= 9:
        if c >= 5:
            return 1
        base = 3 + 2 * k + (2 if c == 3 else 0) + (1 if p == 5 else 0)
        return max(0, min(9, base))
    if 19 <= p <= 28:
        return 4 if (c <= 3 and k >= 3) else (2 if c <= 3 else 0)
    if p >= 32:
        return 6 if c >= 5 else 1
    return 0
