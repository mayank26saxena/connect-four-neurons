def fires(b):
    # opponent has an immediate (playable) winning cell that I must block
    return len(b.their_playable_wins) > 0


def level(b):
    if not fires(b):
        return 0
    cols = set(c for (r, c) in b.their_playable_wins)
    if 1 in cols or 6 in cols:
        return 8
    return 5
