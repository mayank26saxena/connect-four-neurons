def cells(b):
    return [c for (r, c) in (b.their_wins | b.my_wins) if r == 0]

def fires(b):
    return len(cells(b)) > 0

def level(b):
    cs = cells(b)
    if not cs:
        return 0
    if 4 in cs:
        return 9
    if 3 in cs:
        return 7
    return 6
