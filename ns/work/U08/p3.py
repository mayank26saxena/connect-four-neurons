def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def score(b):
    if b.heights[5] == 6 or b.ply < 2:
        return 0
    rec = b.moves[-4:]
    k = sum(1 for m in rec if m == 5)
    s = 0
    if b.last_col == 5:
        s += 3
    s += k
    f = nfull(b)
    s += min(f, 5)
    if b.ply >= 28:
        s += 1
    return s

def fires(b):
    return score(b) >= 8

def level(b):
    return max(0, min(9, score(b) - 3))
