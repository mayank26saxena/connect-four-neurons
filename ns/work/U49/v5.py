def poisoned(b):
    bad = set()
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            bad.add(c)
    return bad

def forced(b):
    # exactly one sensible move: a single must-block, or only one column that does not hand them a win
    if b.my_playable_wins:
        return None
    mb = set(c for (r, c) in b.their_playable_wins)
    if len(mb) == 1:
        c = list(mb)[0]
        return c
    if mb:
        return None
    bad = poisoned(b)
    safe = [c for c in b.legal if c not in bad]
    if len(safe) == 1:
        return safe[0]
    return None

def fires(b):
    f = forced(b)
    if f is None:
        return False
    # the forced cell sits on top of an opponent stone in rows 2-4
    r = b.landing(f)
    return 2 <= r <= 4 and b.grid[r - 1][f] == 2

def level(b):
    f = forced(b)
    if f is None:
        return 0
    r = b.landing(f)
    s = 3
    if 2 <= r <= 4:
        s += 2
    if r >= 1 and b.grid[r - 1][f] == 2:
        s += 2
    if f in (1, 4):
        s += 2
    return s
