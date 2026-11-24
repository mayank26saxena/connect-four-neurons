F4 = [0.0, 0.6, 1.2, 1.8, 2.2]

def col4_term(b):
    h4 = b.heights[4]
    if h4 <= 4:
        return F4[h4]
    f = h4 / b.ply
    if f <= 0.22:
        return 2.2
    if f <= 0.28:
        return 2.2 - (f - 0.22) / 0.06 * 0.5
    if f <= 0.33:
        return 1.7 - (f - 0.28) / 0.05 * 0.7
    return max(-0.5, 1.0 - (f - 0.33) / 0.07 * 1.0)

def score(b):
    h = b.heights
    n012 = h[0] + h[1] + h[2]
    s = 0.12 * min(n012, 9) - 0.05 * h[3] + col4_term(b) - 0.15 * h[5] - 0.35 * (h[6] - 1) + 0.58
    if b.ply < 15:
        s -= 0.15 * (15 - b.ply)
    return s

def fires(b):
    if b.last_col != 6:
        return False
    return score(b) >= 1.8

def level(b):
    if b.last_col != 6:
        return 0
    return int(max(0, min(9, round(score(b) * 3))))
