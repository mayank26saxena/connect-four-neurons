def fires(b):
    # weak proxy: the opponent has an immediate threat I must block
    return len(b.their_playable_wins) > 0 and not b.my_playable_wins

def level(b):
    if b.my_playable_wins:
        return 0
    L = b.landing(3)
    if L is not None and L >= 4 and (L, 3) in b.their_playable_wins:
        return 9
    if b.their_playable_wins:
        return 3
    return 1
