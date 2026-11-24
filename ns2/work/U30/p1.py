def fires(b):
    return b.ply >= 14 and len(b.their_wins) >= 1 and len(b.their_wins) >= len(b.my_wins)

def level(b):
    if b.ply < 14:
        return 0
    d = len(b.their_wins) - len(b.my_wins)
    if len(b.their_wins) == 0:
        return 0
    return max(0, min(9, 3 + 2 * d))
