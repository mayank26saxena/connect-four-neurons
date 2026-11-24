def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def lv(b):
    if len(b.my_playable_wins) > 0:
        return 0
    s = 0
    p = poisoned(b)
    if len(p) > 0:
        s += 2
    if len(p) > 1:
        s += 1
    for (r, c) in b.their_playable_wins:
        s += 4 if c == 2 else (2 if c == 4 else 1)
    if b.ply >= 24:
        s += 1
    if b.ply >= 30:
        s += 1
    nl = len(b.legal)
    if 2 <= nl <= 3:
        s += 2
    elif nl == 4:
        s += 1
    return min(9, s)

def fires(b):
    return lv(b) >= 6

def level(b):
    return lv(b)
