def s(b):
    g = b.grid
    T = lambda r, c: 1 if g[r][c] == 2 else 0
    M = lambda r, c: 1 if g[r][c] == 1 else 0
    v = 2 * (T(0, 3) + T(1, 3) + T(1, 4) + T(2, 5)) + T(1, 5)
    v += 2 * M(2, 4) + M(2, 3) + M(1, 6)
    v -= 2 * T(1, 2)
    if not b.me_first:
        v += 2
    return v

def fires(b):
    return s(b) >= 11

def level(b):
    v = s(b)
    if v <= 7:
        return 0
    if v <= 9:
        return v - 7
    return min(9, (v - 9) * 2 + (1 if b.ply >= 24 else 0))
