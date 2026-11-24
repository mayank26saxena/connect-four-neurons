def score_open(b):
    empty = sum(1 for h in b.heights if h == 0)
    full = sum(1 for h in b.heights if h == 6)
    s = 0
    if b.ply <= 8:
        s += 3
    elif b.ply <= 14:
        s += 2
    elif b.ply <= 20:
        s += 1
    s += min(empty, 3)
    s -= 2 * full
    if b.heights[3] <= 2:
        s += 1
    return s

def fires(b):
    return score_open(b) >= 6

def level(b):
    return max(0, min(9, score_open(b) + 1))
