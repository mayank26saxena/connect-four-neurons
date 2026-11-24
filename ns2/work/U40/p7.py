def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def col2_block(b):
    return any(c == 2 for (r, c) in b.their_playable_wins)

def late(b):
    s = 0
    if len(poisoned(b)) > 0:
        s += 2
    if len(b.their_playable_wins) > 0:
        s += 1
    if b.ply >= 24:
        s += 1
    if b.ply >= 30:
        s += 1
    if 2 <= len(b.legal) <= 3:
        s += 2
    return s

def lv(b):
    if len(b.my_playable_wins) > 0:
        return 0
    s = late(b)
    if col2_block(b):
        s = max(s, 7) + 1
    return min(9, s)

def fires(b):
    return lv(b) >= 7

def level(b):
    return lv(b)
