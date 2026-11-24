def fires(b):
    empty = sum(1 for h in b.heights if h == 0)
    full = sum(1 for h in b.heights if h == 6)
    return full == 0 and empty >= 2 and b.ply >= 6

def level(b):
    empty = sum(1 for h in b.heights if h == 0)
    full = sum(1 for h in b.heights if h == 6)
    s = 0
    if full == 0:
        s += 2
    s += min(empty, 3)
    if len(b.their_playable_wins) > 0:
        s += 2
    return min(9, s)
