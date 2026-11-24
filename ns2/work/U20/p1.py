def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if r + 1 < 6 and (r + 1, c) in b.their_wins and (r, c) not in b.my_wins and (r, c) not in b.their_wins:
            n += 1
    return n

def fires(b):
    return b.ply >= 18 and poisoned(b) > 0

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + (b.ply - 18) // 3 + (2 if b.heights[4] == 6 else 0))
