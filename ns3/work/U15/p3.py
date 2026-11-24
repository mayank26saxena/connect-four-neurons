def fires(b):
    if len(b.legal) < 2:
        return False
    return any(c == 6 and r >= 1 for (r, c) in b.their_playable_wins)

def level(b):
    if len(b.legal) < 2:
        return 0
    if any(c == 6 and r >= 1 for (r, c) in b.their_playable_wins):
        return 8
    if any(c == 0 for (r, c) in b.their_playable_wins):
        return 5
    if b.their_playable_wins:
        return 3
    return 0
