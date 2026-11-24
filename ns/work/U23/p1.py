def fires(b):
    return len(b.their_playable_wins) + len(b.my_playable_wins) > 0

def level(b):
    n = len(b.their_playable_wins) + len(b.my_playable_wins)
    if n >= 2:
        return 9
    if n == 1:
        return 5
    return 0
