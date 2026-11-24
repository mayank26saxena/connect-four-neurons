def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def poisoned(b):
    # legal columns where the cell just above the landing cell completes four for the opponent
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r is not None and r + 1 <= 5 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def score(b):
    h0 = b.heights[0]
    if h0 == 6:
        return 0
    if b.my_playable_wins or b.their_playable_wins:
        return 1
    s = 0
    f = nfull(b)
    if h0 == 5 and f >= 2:
        s += 4
    p = len(poisoned(b))
    if p >= 1 and b.ply >= 14:
        s += 3 + p
    s += min(f, 3) // 2
    return min(9, s)

def fires(b):
    return score(b) >= 4

def level(b):
    return score(b)
