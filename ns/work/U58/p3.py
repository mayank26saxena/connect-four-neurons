def fires(b):
    return len(b.my_wins) > 0 and not b.my_playable_wins and not b.their_playable_wins

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + 2 * len(b.my_wins))
