def score_late(b):
    h = b.heights
    s = (h[2] + h[3] + h[4] + h[5]) - 2 * (h[0] + h[1]) - h[6]
    if b.last_col in (4, 6):
        s += 2
    elif b.last_col in (0, 3, 5):
        s -= 3
    base = {27: 0, 25: -5, 29: -2, 31: -3}
    return s + base[b.ply]

def early(b):
    h = b.heights
    return b.ply == 4 and b.last_col == 5 and h[5] == 1 and h[6] == 0

def fires(b):
    if b.ply in (25, 27, 29, 31):
        return score_late(b) >= 0
    return early(b)

def level(b):
    if b.ply in (25, 27, 29, 31):
        v = 5 + score_late(b) // 2
        return max(0, min(9, v))
    if early(b):
        return 8 if b.heights[4] == 0 else 5
    if b.ply == 4 and b.last_col in (5, 6):
        return 3
    return 0
