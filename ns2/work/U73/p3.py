W = {0: 3.5, 1: 4.0, 2: 0.9, 3: 1.7, 4: 0.3, 5: 2.3, 6: 0.3}
M = {0: -1.0, 1: 0.0, 2: 0.0, 3: 1.0, 4: -0.7, 5: 1.0, 6: 0.0}

def _score(b):
    if b.last_col is None or b.ply < 4:
        return -9
    p = b.ply
    s = W[b.last_col]
    if p % 2 == 0:
        for r in range(6):
            for c in range(7):
                if b.grid[r][c] == 1:
                    s += M[c]
        s -= 0 if p == 4 else (p - 4) + 1.5
    else:
        s -= 2.0 if p == 5 else (p - 5) * 1.2 + 2.0
    return s

def fires(b):
    return _score(b) >= 1.5

def level(b):
    s = _score(b)
    return max(0, min(9, int(round(s * 1.3 + 1))))
