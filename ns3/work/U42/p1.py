def fires(b):
    return any(c == 0 for (r, c) in b.their_playable_wins)

def level(b):
    if fires(b):
        return 9 if b.last_col == 0 else 6
    if b.their_playable_wins:
        return 1
    return 0
