def fires(b):
    return len(b.their_playable_wins) > 0

def level(b):
    if not b.their_playable_wins:
        return 0
    if (b.heights[3], 3) in b.their_playable_wins:
        return 9
    return 5
