def fires(b):
    if b.my_playable_wins:
        return False
    return b.heights[1] <= 1 and len(b.their_playable_wins) > 0

def level(b):
    if not fires(b):
        return 0
    return 6
