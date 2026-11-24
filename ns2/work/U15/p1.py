def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def fires(b):
    return len(poisoned(b)) > 0

def level(b):
    p = poisoned(b)
    if not p:
        return 0
    return min(9, 3 + (7 - len(b.legal)) + (2 if b.their_playable_wins else 0))
