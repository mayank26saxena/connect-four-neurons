F4 = [0.0, 0.6, 1.2, 1.8, 2.2, 1.7, 1.0]

def score(b):
    h = b.heights
    n012 = h[0] + h[1] + h[2]
    s = 0.12 * min(n012, 9) - 0.05 * h[3] + F4[h[4]] - 0.15 * h[5] - 0.15 * (h[6] - 1) + 0.58
    if b.ply < 15:
        s -= 0.15 * (15 - b.ply)
    return s

def fires(b):
    if b.last_col != 6:
        return False
    return score(b) >= 1.6

def level(b):
    if b.last_col != 6:
        return 0
    s = score(b)
    return int(max(0, min(9, round(s * 3))))
