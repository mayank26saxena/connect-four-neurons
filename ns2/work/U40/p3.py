def loses(b, c):
    # after I play c, the opponent can win at once
    r = b.landing(c)
    for cell in b.their_playable_wins:
        if cell != (r, c):
            return True
    return (r + 1, c) in b.their_wins

def nsafe(b):
    return sum(1 for c in b.legal if not loses(b, c))

def fires(b):
    if len(b.my_playable_wins) > 0 or len(b.legal) < 2:
        return False
    return nsafe(b) == 0

def level(b):
    if len(b.my_playable_wins) > 0 or len(b.legal) < 2:
        return 0
    n = nsafe(b)
    if n == 0:
        return 7 + min(2, len(b.legal) - 2)
    if n == 1 and len(b.legal) >= 3:
        return 3
    return 0
