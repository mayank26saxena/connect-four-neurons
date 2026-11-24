def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def score(b):
    h5 = b.heights[5]
    if h5 == 6:
        return 0
    f = nfull(b)
    if b.last_col != 5:
        if b.last_col in (2, 4, 6) and f >= 3 and 2 <= h5 <= 4:
            return 3
        return 0
    s = 2
    if 2 <= h5 <= 4:
        s += 1
    if h5 == 3:
        s += 1
    if not b.me_first:
        s += 1
    s += min(f, 5)
    return s

def fires(b):
    return score(b) >= 6

def level(b):
    return max(0, min(9, score(b)))
