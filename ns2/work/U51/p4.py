def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins and (r, c) not in b.my_wins:
            n += 1
    return n

def fires(b):
    return poisoned(b) >= 1 and len(b.my_wins) == 0

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + b.ply // 6 + poisoned(b))
