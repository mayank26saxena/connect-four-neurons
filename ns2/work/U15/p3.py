def endgame(b):
    h = b.heights
    open45 = (h[4] < 6) + (h[5] < 6)
    if open45 == 0:
        return 0
    s = 0
    s += 3 if h[1] == 6 else (1 if h[1] == 5 else 0)
    s += 2 if h[0] == 6 else (1 if h[0] == 5 else 0)
    s += 1 if h[2] == 6 else 0
    s += 1 if h[3] == 6 else 0
    s += 1 if h[6] == 6 else 0
    if open45 == 1:
        s -= 2
    return max(0, s)

def threat(b):
    pw = b.their_playable_wins
    if len(pw) >= 2:
        return 7
    if any(c == 3 for (r, c) in pw):
        return 5
    return 0

def level(b):
    return max(0, min(9, max(endgame(b), threat(b))))

def fires(b):
    return level(b) >= 5
