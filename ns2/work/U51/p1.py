def hits(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r, c) in b.their_wins or (r + 1, c) in b.their_wins:
            n += 1 if c in (0, 1, 5, 6) else 2
    return n

def fires(b):
    return hits(b) >= 2

def level(b):
    return min(9, hits(b) * 3)
