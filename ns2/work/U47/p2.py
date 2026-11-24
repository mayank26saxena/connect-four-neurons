def fires(b):
    if b.my_playable_wins:
        return False
    if b.heights[1] > 1 and b.heights[1] < 6:
        return False
    return any(c in (0, 2) and r >= 2 for (r, c) in b.their_wins)

def level(b):
    if not fires(b):
        return 0
    if (3, 2) in b.their_wins or (3, 0) in b.their_playable_wins:
        return 9
    return 6
