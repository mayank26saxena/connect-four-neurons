def fires(b):
    return level(b) >= 5

def level(b):
    if b.my_playable_wins:
        return 0
    w = list(b.their_playable_wins)
    if len(w) != 1:
        return 0
    r, c = w[0]
    if r == 0 and c != 3:
        return 9
    return 0
