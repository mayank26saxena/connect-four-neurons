def counts(b):
    t = [0]*7
    m = [0]*7
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                m[c] += 1
            elif v == 2:
                t[c] += 1
    return t, m

def sB(b):
    t, m = counts(b)
    L = b.last_col
    t3 = t[3] - (1 if L == 3 else 0)
    lb = {3: 4, 2: 1, 1: 1}.get(L, -1)
    return 2.5*m[5] + 1.5*m[6] - 0.5*m[0] - 0.5*m[4] + 1.0*t[2] + 0.3*t[0] - 2*t3 - 0.5*t[4] - 0.5*t[6] + lb

def sA(b):
    t, m = counts(b)
    L = b.last_col
    if L not in (0, 1):
        return -99
    base = 4 if L == 1 else 1
    return base + 2*m[0] + 1.5*t[3] + 1.5*t[4] + 1.0*t[6] - 2*m[5] - 1*m[6] - 1.5*t[2] - 0.3*b.ply

def fires(b):
    if b.last_col is None:
        return False
    return sB(b) >= 10 or sA(b) >= 4

def level(b):
    if b.last_col is None:
        return 0
    s = max(sB(b) - 10, sA(b) - 4)
    if s < -4:
        return 0
    return max(0, min(9, int(s + 5)))
