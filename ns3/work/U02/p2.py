def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r is not None and r + 1 < 6 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def fires(b):
    return len(poisoned(b)) > 0

def level(b):
    p = poisoned(b)
    if not p:
        return 0
    return min(9, 4 + 2 * len(p))
