def fires(b):
    if b.ply <= 9:
        return len(b.their_playable_wins) >= 2 or len(b.my_playable_wins) >= 2
    if b.ply < 28:
        return False
    if len(b.my_playable_wins) > 0:
        return False
    return len(b.legal) <= 3

def level(b):
    if not fires(b):
        if b.ply >= 28:
            return 2
        return 0
    empty = 42 - b.ply
    return min(9, 4 + (5 - len(b.legal)) + (1 if empty >= 6 else 0))
