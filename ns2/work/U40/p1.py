def unsafe(b, c):
    r = b.landing(c)
    pb = b.their_playable_wins
    if len(pb) > 0 and (r, c) not in pb:
        return True
    if len(pb) > 1:
        return True
    if (r + 1, c) in b.their_wins:
        return True
    return False

def nsafe(b):
    return sum(1 for c in b.legal if not unsafe(b, c))

def fires(b):
    if len(b.my_playable_wins) > 0:
        return False
    return nsafe(b) == 0

def level(b):
    if len(b.my_playable_wins) > 0:
        return 0
    n = nsafe(b)
    if n == 0:
        return 8
    if n == 1:
        return 4
    return 0
