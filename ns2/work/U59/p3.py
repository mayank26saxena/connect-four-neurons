def opening(b):
    h = b.heights
    return b.ply <= 6 and h[3] == 0 and h[4] == 0 and h[2] > 0 and h[5] > 0

def worse(b):
    return len(b.their_wins) > 0 and len(b.my_wins) == 0 and b.ply <= 20

def fires(b):
    return opening(b) or worse(b)

def level(b):
    if opening(b):
        return 8
    if worse(b):
        return 6 if len(b.their_playable_wins) > 0 else 4
    if len(b.my_wins) == 0:
        return 2
    return 0
