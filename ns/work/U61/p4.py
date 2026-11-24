def score_of(b):
    g = b.grid
    if b.ply == 1:
        return 3.0 if g[0][1] == 2 else 0.0
    if b.ply > 15:
        return 0.0
    def t(r, c):
        return 1.0 if g[r][c] == 2 else 0.0
    s = 2.0 * t(0, 5) + 1.5 * t(0, 1) + 0.7 * t(0, 4) + 0.7 * t(0, 3) + 1.0 * t(1, 3)
    s += 0.5 * t(3, 3)
    s += 1.0 if g[0][2] == 1 else -1.0
    s -= 1.0 * t(0, 0) + 3.0 * t(0, 6)
    s -= 0.1 * b.ply
    return s

def fires(b):
    return score_of(b) >= 2.8

def level(b):
    s = score_of(b)
    if s < 1.8:
        return 0
    return max(0, min(9, int((s - 1.8) * 3)))
