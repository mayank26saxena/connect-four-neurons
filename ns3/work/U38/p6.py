def row0(wins):
    return len([w for w in wins if w[0] == 0])

def bottom(b):
    m = row0(b.my_playable_wins)
    t = row0(b.their_playable_wins)
    if m >= 2 or t >= 2:
        return 2
    if m + t >= 1:
        return 1
    return 0

def mid_block(b):
    return any(r > 0 and 2 <= c <= 3 for (r, c) in b.their_playable_wins)

def fires(b):
    return bottom(b) > 0 or mid_block(b)

def level(b):
    k = bottom(b)
    if k == 2:
        return 9
    if k == 1:
        return 5
    if mid_block(b):
        return 3
    if len(b.my_playable_wins) + len(b.their_playable_wins) > 0:
        return 1
    return 0
