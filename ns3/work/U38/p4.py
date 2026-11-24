def row0_wins(b):
    m = len([w for w in b.my_playable_wins if w[0] == 0])
    t = len([w for w in b.their_playable_wins if w[0] == 0])
    return m, t

def row0_setup(b):
    # one more stone on the bottom row would make an open three _SSS_ for one side
    g = b.grid[0]
    for s in (1, 2):
        for c in range(3):
            if g[c] == 0 and g[c + 4] == 0:
                mid = [g[c + 1], g[c + 2], g[c + 3]]
                if mid.count(s) == 2 and mid.count(0) == 1:
                    return True
    return False

def fires(b):
    m, t = row0_wins(b)
    return m + t > 0 or row0_setup(b)

def level(b):
    m, t = row0_wins(b)
    if m >= 2 or t >= 2:
        return 9
    if m + t > 0:
        return 5
    if row0_setup(b):
        return 4
    if len(b.my_playable_wins) + len(b.their_playable_wins) > 0:
        return 2
    return 0
