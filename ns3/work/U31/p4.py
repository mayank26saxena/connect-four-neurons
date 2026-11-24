def poisoned(b):
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins and (r + 1, c) not in b.my_wins:
            n += 1
    return n

def fires(b):
    return level(b) >= 5

def level(b):
    if b.my_playable_wins or len(b.their_playable_wins) >= 2:
        return 0
    if b.their_playable_wins:
        r, c = list(b.their_playable_wins)[0]
        if r == 0 and c != 3:
            return 9
        return 2
    n = poisoned(b)
    if n >= 2:
        return 7
    if n == 1:
        return 5
    return 0
