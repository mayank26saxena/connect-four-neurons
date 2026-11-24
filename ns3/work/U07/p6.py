def col1_level(b):
    L = b.landing(1)
    if L is None:
        return 0
    w = b.my_wins
    t = [d for d in range(3) if (L + d, 1) in w]
    if not t:
        return 0
    if 0 in t:
        return 8
    if 1 in t and 2 in t:
        return 8
    if len(w) >= 2:
        return 6
    return 0

def stacked(b):
    w = b.my_wins
    return any((r + 1, c) in w and (r, c) not in b.their_wins for (r, c) in w)

def fires(b):
    if col1_level(b):
        return True
    if b.ply < 12:
        return False
    if b.my_playable_wins and len(b.my_wins) >= 2:
        return True
    return stacked(b)

def level(b):
    lv = col1_level(b)
    if lv:
        return lv
    if fires(b):
        return 5
    if b.my_playable_wins:
        return 2
    return 0
