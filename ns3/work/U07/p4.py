def col1_threats(b):
    L = b.landing(1)
    if L is None:
        return []
    return [d for d in range(3) if (L + d, 1) in b.my_wins]

def stacked(b):
    w = b.my_wins
    return any((r + 1, c) in w and (r, c) not in b.their_wins for (r, c) in w)

def fires(b):
    if col1_threats(b):
        return True
    if b.my_playable_wins and b.ply >= 14:
        return True
    return stacked(b)

def level(b):
    t = col1_threats(b)
    lv = 0
    if t:
        lv = 5 + 2 * len(t)
    elif b.my_playable_wins and b.ply >= 14:
        lv = 4
    elif stacked(b):
        lv = 4
    return min(9, lv)
