def row0_wins(b):
    m = len([w for w in b.my_playable_wins if w[0] == 0])
    t = len([w for w in b.their_playable_wins if w[0] == 0])
    return m, t

def central_block(b):
    return any(2 <= c <= 4 for (r, c) in b.their_playable_wins)

def fires(b):
    m, t = row0_wins(b)
    return m + t > 0 or central_block(b)

def level(b):
    m, t = row0_wins(b)
    if m >= 2 or t >= 2:
        return 9
    if m + t > 0:
        return 5
    if central_block(b):
        return 3
    if len(b.my_playable_wins) + len(b.their_playable_wins) > 0:
        return 1
    return 0
