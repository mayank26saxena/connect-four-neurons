def fires(b):
    return level(b) >= 5

def level(b):
    if b.my_playable_wins or len(b.their_playable_wins) >= 2:
        return 0
    if b.their_playable_wins:
        r, c = list(b.their_playable_wins)[0]
        if c == 3:
            return 0
        return 8 if r == 0 else 5
    r3 = b.landing(3)
    if r3 is None:
        return 5
    if (r3 + 1, 3) in b.their_wins:
        return 6
    return 0
