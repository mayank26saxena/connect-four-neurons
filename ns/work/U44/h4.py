def col4_tactic(b):
    n = 0
    for (r, c) in b.my_playable_wins:
        if c == 4:
            n += 1
    for (r, c) in b.their_playable_wins:
        if c == 4:
            n += 1
    return n

def tower(b):
    h = b.heights
    return min(h[2], h[3]) - max(h[1], h[4])

def fires(b):
    return col4_tactic(b) >= 1

def level(b):
    s = 0
    if col4_tactic(b) >= 1:
        s += 5
    t = tower(b)
    if t >= 2:
        s += 2 + min(2, t - 2)
    return min(9, s)
