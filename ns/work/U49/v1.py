def losing_cols(b):
    bad = set()
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            bad.add(c)
    return bad

def forced_col(b):
    if b.my_playable_wins:
        return None
    mb = set(c for (r, c) in b.their_playable_wins)
    if len(mb) == 1:
        return list(mb)[0]
    if len(mb) > 1:
        return None
    safe = [c for c in b.legal if c not in losing_cols(b)]
    if len(safe) == 1:
        return safe[0]
    return None

def fires(b):
    return forced_col(b) == 1

def level(b):
    f = forced_col(b)
    if f == 1:
        return 7
    if f == 4:
        return 3
    return 0
