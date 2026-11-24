def poisoned(b, c):
    h = b.heights[c]
    return h < 5 and (h + 1, c) in b.their_wins

def fires(b):
    if b.my_playable_wins:
        return False
    if 1 < b.heights[1] < 6:
        return False
    if b.their_playable_wins:
        return True
    return poisoned(b, 2) or poisoned(b, 1) or poisoned(b, 6) or poisoned(b, 0)

def level(b):
    if not fires(b):
        return 0
    s = 5
    if poisoned(b, 2):
        s += 3
    if b.heights[1] <= 1:
        s += 1
    return min(9, s)
