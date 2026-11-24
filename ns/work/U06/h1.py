def fires(b):
    return any(c == 0 for (r, c) in b.their_playable_wins)

def level(b):
    if not fires(b):
        return 0
    if b.my_playable_wins:
        return 5
    return 9
