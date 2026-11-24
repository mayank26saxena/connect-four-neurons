def cells(b):
    return [c for (r, c) in (b.their_wins | b.my_wins) if r == 0 and c >= 2]

def low(b):
    return [(r, c) for (r, c) in (b.their_playable_wins | b.my_playable_wins) if 1 <= r <= 2]

def fires(b):
    return len(cells(b)) > 0 or len(low(b)) > 0

def level(b):
    cs = cells(b)
    if 4 in cs:
        return 9
    if cs:
        return 7
    if low(b):
        return 3
    return 0
