def fires(b):
    return len(b.their_playable_wins) >= 1

def level(b):
    n = len(b.their_playable_wins)
    t = min(len(b.their_wins), 4)
    return min(9, 3 * n + t)
