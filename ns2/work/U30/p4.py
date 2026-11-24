def fires(b):
    return b.heights[4] == 6 and len(b.their_wins) >= 1

def level(b):
    if b.heights[4] != 6:
        return 0
    t = len(b.their_wins)
    if t == 0:
        return 2
    return min(9, 4 + t)
