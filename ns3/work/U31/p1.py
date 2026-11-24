def fires(b):
    return level(b) >= 4

def level(b):
    if b.my_playable_wins:
        return 0
    n = len(b.their_playable_wins)
    if n >= 2:
        return 0
    if n == 1:
        r, c = list(b.their_playable_wins)[0]
        return 8 if r == 0 else 5
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            return 4
    return 0
