def unsafe(b, c):
    r = b.landing(c)
    left = [w for w in b.their_playable_wins if w != (r, c)]
    if len(left) > 0:
        return True
    return (r + 1, c) in b.their_wins

def col4_poison(b):
    return b.heights[4] == 0 and (1, 4) in b.their_wins

def all_lost(b):
    if len(b.my_playable_wins) > 0 or len(b.legal) == 0:
        return False
    return all(unsafe(b, c) for c in b.legal)

def fires(b):
    return col4_poison(b) or all_lost(b)

def level(b):
    if col4_poison(b):
        return 9
    if all_lost(b):
        return 5
    return 0
