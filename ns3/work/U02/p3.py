def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r < 5 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def fires(b):
    return len(poisoned(b)) > 0 and nfull(b) >= 4

def level(b):
    p = len(poisoned(b))
    f = nfull(b)
    if p == 0:
        return min(3, f // 2)
    return max(0, min(9, f + p))
