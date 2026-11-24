def fires(b):
    return b.ply == 0

def level(b):
    if b.ply == 0:
        return 9
    if len(b.their_playable_wins) >= 2:
        return 5
    if len(b.their_playable_wins) == 1:
        return 3
    return 2
