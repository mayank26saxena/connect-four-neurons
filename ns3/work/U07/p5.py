def col1_level(b):
    L = b.landing(1)
    if L is None:
        return 0
    w = b.my_wins
    if (L, 1) in w and b.ply >= 12:
        return 8
    if (L + 1, 1) in w and (L + 2, 1) in w:
        return 8
    if (L + 1, 1) in w and (L + 1, 1) not in b.their_wins and len(w) >= 2:
        return 6
    return 0

def fires(b):
    return col1_level(b) > 0

def level(b):
    lv = col1_level(b)
    if lv:
        return lv
    L = b.landing(1)
    if L is not None and any((L + d, 1) in b.my_wins for d in range(3)):
        return 3
    if b.my_playable_wins and b.ply >= 14:
        return 2
    return 0
