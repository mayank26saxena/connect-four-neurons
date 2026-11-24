def poisoned(b):
    # columns where the opponent has a winning cell directly above my landing cell
    out = []
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def lv(b):
    s = 0
    p = poisoned(b)
    if len(p) > 0:
        s += 5
    if len(p) > 1:
        s += 1
    for (r, c) in b.their_playable_wins:
        if c == 2:
            s += 6
        elif c == 4:
            s += 3
        else:
            s += 1
    if len(b.my_playable_wins) > 0:
        s -= 4
    return max(0, min(9, s))

def fires(b):
    return lv(b) >= 5

def level(b):
    return lv(b)
