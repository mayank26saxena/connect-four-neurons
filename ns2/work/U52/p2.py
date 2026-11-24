def _w(b):
    t = set(b.their_wins) | set(b.my_wins)
    s = 0
    if (0, 1) in t and (0, 5) in t:
        s += 4
    for r in range(1, 6):
        if (r, 4) in t:
            s += 2
    if len(b.their_playable_wins) >= 1:
        s += 1
    return s

def fires(b):
    return _w(b) >= 3

def level(b):
    return min(9, _w(b) * 2)
