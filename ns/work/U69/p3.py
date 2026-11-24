def diff(b):
    return len(b.their_wins) - len(b.my_wins)

def fires(b):
    return b.ply >= 26 and len(b.their_wins) >= 2 and diff(b) >= 1

def level(b):
    if not fires(b):
        return 0
    d = diff(b)
    return min(9, 3 + 2 * d + (1 if b.ply >= 32 else 0))
