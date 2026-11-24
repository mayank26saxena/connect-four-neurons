def score_share(b):
    w = [1.0, 0.0, 0.2, 0.0, 1.0, -1.0, -0.7]
    tot = 0
    s = 0.0
    for c in range(7):
        for r in range(6):
            if b.grid[r][c] == 1:
                tot += 1
                s += w[c]
    if tot == 0:
        return 0.0
    return s / tot

def fires(b):
    if b.last_col not in (1, 5):
        return False
    return score_share(b) >= 0.4

def level(b):
    if b.last_col not in (1, 5):
        return 0
    x = score_share(b)
    if x < 0.1:
        return 0
    return max(0, min(9, int(x * 10)))
