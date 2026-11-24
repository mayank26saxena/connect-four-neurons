def fires(b):
    return len(b.their_playable_wins) > 0 and len(b.my_playable_wins) == 0 and len(b.legal) > 1

def level(b):
    if not fires(b):
        return 0
    if len(b.their_playable_wins) >= 2:
        return 9
    c = list(b.their_playable_wins)[0][1]
    return {0: 2, 1: 3, 2: 7, 3: 5, 4: 7, 5: 3, 6: 2}[c]
