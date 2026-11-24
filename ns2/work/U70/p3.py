def col4_poison(b):
    return b.heights[4] == 0 and (1, 4) in b.their_wins

def poisoned_cols(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r, c) in b.their_playable_wins:
            continue
        if (r + 1, c) in b.their_wins:
            n += 1
    return n

def fires(b):
    if col4_poison(b):
        return True
    return poisoned_cols(b) >= 1 and b.heights[4] == 6

def level(b):
    if col4_poison(b):
        return 9
    if fires(b):
        return 4
    return 0
