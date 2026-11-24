def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            n += 1
    return n

def fires(b):
    return poisoned(b) >= 1

def level(b):
    n = poisoned(b)
    if n == 0:
        return 0
    return min(9, 3 + 3 * n)
