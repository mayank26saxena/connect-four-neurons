def col0_threats(b):
    # (distance above column-0 landing cell, row) for each of my winning cells in column 0
    h = b.landing(0)
    if h is None:
        return []
    return [(r - h, r) for (r, c) in b.my_wins if c == 0]

def good_parity(b, r):
    # first player profits from threats on rows 1,3,5 (index 0,2,4); second player from rows 2,4,6
    return (r % 2 == 0) == bool(b.me_first)

def fires(b):
    for (d, r) in col0_threats(b):
        if d == 0:
            return True
        if d == 1 and good_parity(b, r):
            return True
    return len(b.my_playable_wins) >= 2

def level(b):
    v = 0
    for (d, r) in col0_threats(b):
        if d == 0:
            v = max(v, 6)
        elif d == 1:
            v = max(v, 5 if good_parity(b, r) else 1)
        elif d == 2:
            v = max(v, 1)
    if v > 0:
        v += min(3, len(b.my_wins) - 1)
    elif len(b.my_playable_wins) >= 2:
        v = 3
    return min(9, v)
