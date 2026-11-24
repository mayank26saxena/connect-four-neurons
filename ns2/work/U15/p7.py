def closed_score(b):
    h = b.heights
    s = 0.0
    for c in (0, 1):
        if h[c] == 6:
            s += 3
        elif h[c] == 5:
            s += 1.5
    s += 1.5 * (h[2] == 6) + 1.0 * (h[3] == 6) + 1.0 * (h[6] == 6)
    s -= 2.0 * (h[4] == 6) + 1.0 * (h[5] == 6)
    return s

def level(b):
    s = closed_score(b)
    lv = int(s) - 1
    if len(b.their_playable_wins) >= 2 and b.ply <= 14:
        lv = max(lv, 7)
    return max(0, min(9, lv))

def fires(b):
    return level(b) >= 6
