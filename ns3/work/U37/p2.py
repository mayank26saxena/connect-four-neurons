def fires(b):
    if b.my_playable_wins or b.their_playable_wins:
        return False
    return len(b.legal) <= 4 and 0 in b.legal

def level(b):
    if b.my_playable_wins or b.their_playable_wins or 0 not in b.legal:
        return 0
    n = len(b.legal)
    return max(0, min(9, 2 * (7 - n) - 1))
