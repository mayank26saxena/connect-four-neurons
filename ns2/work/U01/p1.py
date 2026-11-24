def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if r is not None and r + 1 < 6 and (r + 1, c) in b.their_wins:
            n += 1
    return n

def fires(b):
    return poisoned(b) > 0

def level(b):
    return min(9, 6 * poisoned(b))
