def loses(b, c):
    # after I play c the opponent can win at once
    r = b.landing(c)
    for cell in b.their_playable_wins:
        if cell != (r, c):
            return True
    return (r + 1, c) in b.their_wins

def nsafe(b):
    return sum(1 for c in b.legal if not loses(b, c))

def lv(b):
    if len(b.my_playable_wins) > 0:
        return 0
    s = 0
    if any((b.landing(c) + 1, c) in b.their_wins for c in b.legal):
        s += 2
    if len(b.their_playable_wins) > 0:
        s += 1
    if b.ply >= 24:
        s += 1
    if b.ply >= 30:
        s += 1
    if 2 <= len(b.legal) <= 3:
        s += 2
    if nsafe(b) == 0:
        s += 2
    return min(9, s)

def fires(b):
    return lv(b) >= 7

def level(b):
    return lv(b)
