def col4_tactic(b):
    n = 0
    for (r, c) in b.my_playable_wins:
        if c == 4:
            n += 1
    for (r, c) in b.their_playable_wins:
        if c == 4:
            n += 1
    return n

def pairs23(b):
    g = b.grid
    n = 0
    for r in range(6):
        if g[r][2] != 0 and g[r][2] == g[r][3] and g[r][1] == 0 and g[r][4] == 0:
            n += 1
    return n

def tower(b):
    h = b.heights
    return min(h[2], h[3]) - max(h[1], h[4])

def fires(b):
    if col4_tactic(b) >= 1:
        return True
    return tower(b) >= 3 and pairs23(b) >= 2

def level(b):
    s = 0
    if col4_tactic(b) >= 1:
        s += 5
    t = tower(b)
    if t >= 2:
        s += min(4, t - 1) + min(2, pairs23(b))
    return min(9, s)
