def col1_threats(b):
    L = b.landing(1)
    if L is None:
        return []
    return [d for d in range(3) if (L + d, 1) in b.my_wins]

def fires(b):
    return len(col1_threats(b)) > 0

def level(b):
    t = col1_threats(b)
    if not t:
        return 0
    lv = 3 + 2 * len(t)
    if 0 in t:
        lv += 1
    return min(9, lv)
