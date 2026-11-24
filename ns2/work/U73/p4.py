W = {0: 3.5, 1: 4.0, 2: 0.9, 3: 1.7, 4: 0.3, 5: 2.3, 6: 0.3}
M = {0: -1.3, 1: 0.0, 2: 0.0, 3: 1.0, 4: -0.9, 5: 1.0, 6: 0.0}
D = {4: 0.0, 5: 2.0, 6: 3.5, 7: 5.5, 8: 4.5, 9: 6.5, 10: 5.5}

def _score(b):
    if b.last_col is None or b.ply < 4:
        return -9
    p = b.ply
    s = W[b.last_col]
    m = 0.0
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == 1:
                m += M[c]
            elif b.grid[r][c] == 2 and c == 0 and not (c == b.last_col and r == b.last_row):
                s += 0.5
    s += min(m, 2.0)
    if p in D:
        s -= D[p]
    else:
        s -= (p - 4.5) if p % 2 == 0 else (p - 2.5)
    return s

def fires(b):
    return _score(b) >= 1.5

def level(b):
    s = _score(b)
    return max(0, min(9, int(round(s * 1.3 + 1))))
