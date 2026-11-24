def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            n += 1
    return n

def fires(b):
    return (not b.me_first) and poisoned(b) >= 1 and b.ply >= 15

def level(b):
    if b.me_first:
        return 0
    p = poisoned(b)
    if p == 0:
        return 1 if b.their_wins else 0
    return min(9, 3 + 3 * p)
