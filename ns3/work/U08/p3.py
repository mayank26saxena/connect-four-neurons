def cells(b):
    return [c for (r, c) in (b.their_wins | b.my_wins) if r == 0 and c >= 2]

def fires(b):
    return len(cells(b)) > 0

def level(b):
    cs = cells(b)
    if not cs:
        return 0
    if 4 in cs:
        return 9
    return 6
