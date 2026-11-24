def unsafe(b, c):
    r = b.landing(c)
    pb = b.their_playable_wins
    if len(pb) > 1:
        return True
    if len(pb) == 1 and (r, c) not in pb:
        return True
    if (r + 1, c) in b.their_wins:
        return True
    return False

def nsafe(b):
    return sum(1 for c in b.legal if not unsafe(b, c))

def stacked(b):
    for (r, c) in b.their_wins:
        if (r + 1, c) in b.their_wins:
            return True
    return False

def lostish(b):
    s = 0
    if len(b.their_playable_wins) >= 2:
        s += 2
    if nsafe(b) == 0:
        s += 2
    if stacked(b):
        s += 1
    for (r, c) in b.their_playable_wins:
        if (r + 1, c) in b.their_wins:
            s += 1
    return s

def fires(b):
    if len(b.my_playable_wins) > 0 or len(b.legal) < 2:
        return False
    return lostish(b) >= 1

def level(b):
    if len(b.my_playable_wins) > 0 or len(b.legal) < 2:
        return 0
    return min(9, 3 * lostish(b))
