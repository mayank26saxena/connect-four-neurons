def lv(b):
    if len(b.my_playable_wins) > 0:
        return 0
    s = 0
    if b.ply >= 24:
        s += 2
    if b.ply >= 30:
        s += 1
    nl = len(b.legal)
    if nl <= 3:
        s += 2
    if nl == 2 or nl == 3:
        s += 1
    if len(b.their_playable_wins) > 0:
        s += 1
    if len(b.their_wins) >= 2:
        s += 1
    return s

def fires(b):
    return lv(b) >= 7

def level(b):
    return min(9, lv(b))
