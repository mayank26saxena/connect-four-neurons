def fires(b):
    return any(c == 6 for (r, c) in b.their_playable_wins)

def level(b):
    if any(c == 6 for (r, c) in b.their_playable_wins):
        return 9
    if b.their_playable_wins:
        return 2
    return 0
