def fires(b):
    return level(b) >= 5

def level(b):
    if b.my_playable_wins or len(b.their_playable_wins) >= 2:
        return 0
    if b.their_playable_wins:
        r, c = list(b.their_playable_wins)[0]
        if r == 0 and c != 3:
            return 9
    if b.landing(3) is None:
        n = len(b.legal)
        if n <= 2:
            return 7
        if n == 3:
            return 5
        if n == 4:
            return 3
        return 1
    return 0
