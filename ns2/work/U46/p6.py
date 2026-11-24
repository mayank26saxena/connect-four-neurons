def score_late(b):
    h = b.heights
    s = (h[3] + h[4]) - (h[0] + h[1])
    if b.last_col in (4, 6):
        s += 1
    elif b.last_col in (0, 3, 5):
        s -= 2
    base = {27: 3, 25: 0, 29: 0, 31: -1, 33: -2}
    return s + base[b.ply]

def early(b):
    h = b.heights
    return b.ply == 4 and b.last_col == 5

def fires(b):
    if b.ply in (25, 27, 29, 31, 33):
        return score_late(b) >= 6
    return early(b)

def level(b):
    if b.ply in (25, 27, 29, 31, 33):
        v = score_late(b) - 3
        return max(0, min(9, v))
    if early(b):
        return 8 if b.heights[4] == 0 else 5
    if b.ply == 4 and b.last_col in (5, 6):
        return 3
    return 0
