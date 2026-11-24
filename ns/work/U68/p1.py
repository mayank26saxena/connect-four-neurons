def fires(b):
    return any(c in (0, 2, 4) for (r, c) in b.their_playable_wins)

def level(b):
    if not fires(b):
        return 0
    cs = [c for (r, c) in b.their_playable_wins]
    return 9 if 0 in cs else 6
