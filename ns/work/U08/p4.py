def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def score(b):
    if b.last_col != 5 or b.heights[5] == 6:
        return 0
    h5 = b.heights[5]
    s = 2
    if 2 <= h5 <= 4:
        s += 2
    if h5 == 3:
        s += 1
    if not b.me_first:
        s += 2
    s += min(nfull(b), 5) // 2 + (1 if nfull(b) >= 2 else 0)
    return s

def fires(b):
    return score(b) >= 8

def level(b):
    return max(0, min(9, score(b)))
