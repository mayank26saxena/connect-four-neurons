def score_(b):
    s = 0.0
    if b.last_col == 4:
        s += 0.4
    elif b.last_col == 5 or b.last_col == 2:
        s += 0.1
    if b.heights[5] == 0:
        s += 0.3
    if b.ply <= 8:
        s += 0.3
    elif b.ply <= 14:
        s += 0.15
    return s

def fires(b):
    return score_(b) >= 0.85

def level(b):
    return min(9, int(score_(b) * 9))
