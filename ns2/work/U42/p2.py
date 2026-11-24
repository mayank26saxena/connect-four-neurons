def fires(b):
    return level(b) >= 5

def level(b):
    p = b.ply
    c = b.last_col
    r = b.last_row
    if c is None or r is None:
        return 0
    if p % 2 == 0 and p <= 14:
        s = 5
        if p >= 14:
            s = 3
        if c in (3, 4) and r <= 2:
            s += 2
        elif c in (0, 6) and r == 0 and p <= 6:
            s -= 3
        elif c == 2 or r >= 3:
            s -= 2
        return max(0, min(9, s))
    if p == 5:
        return 5 if c not in (0, 2) else 3
    if p % 2 == 1 and p >= 23:
        if c == 0:
            return [1, 2, 3, 5, 7, 9][r]
        if c == 6 and (r >= 4 or r <= 1):
            return 6
        if c == 1 and 2 <= r <= 3:
            return 5
        if c == 4 and 1 <= r <= 3:
            return 5
        return 3
    if p % 2 == 1 and p >= 19:
        return 4 if c == 0 and r >= 3 else 2
    return 1
