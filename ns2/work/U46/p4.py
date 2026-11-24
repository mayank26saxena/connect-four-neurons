LATE = {27: 3, 25: 7, 29: 4, 31: 6}

def score_late(b):
    h = b.heights
    s = 2 * h[3] + h[4] + h[5] - h[0] - 2 * h[1] - h[6]
    if b.last_col in (4, 6):
        s += 2
    elif b.last_col == 5:
        s -= 4
    elif b.last_col in (0, 3):
        s -= 3
    return s - LATE[b.ply]

def score_early(b):
    # ply 4, last stone in column 5; earlier stones in columns 4/5 suppress it
    if b.ply != 4 or b.last_col != 5:
        return -9
    h = b.heights
    return 2 - 2 * h[4] - (h[5] - 1)

def fires(b):
    if b.ply in LATE:
        return score_late(b) >= 0
    return score_early(b) >= 1

def level(b):
    if b.ply in LATE:
        return max(0, min(9, 5 + score_late(b) // 2))
    e = score_early(b)
    if e > -9:
        return max(0, min(9, 4 + 2 * e))
    return 0
