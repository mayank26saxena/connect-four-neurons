def endgame(b):
    h = b.heights
    if h[4] == 6 and h[5] == 6:
        return 0
    s = 0
    s += 3 if h[1] == 6 else (1 if h[1] == 5 else 0)
    s += 2 if h[0] == 6 else (1 if h[0] == 5 else 0)
    s += 1 if h[2] == 6 else 0
    s += 1 if h[3] == 6 else 0
    s += 1 if h[6] == 6 else 0
    if h[4] == 6:
        s -= 3
    elif h[5] == 6:
        s -= 1
    return max(0, s)

def level(b):
    s = endgame(b)
    if len(b.their_playable_wins) >= 2:
        s = max(s, 6)
    return min(9, s)

def fires(b):
    return level(b) >= 5
