def bottom_block(b):
    # exactly one must-block, on the bottom row, not in the centre column, and no win of my own
    if b.my_playable_wins:
        return False
    w = list(b.their_playable_wins)
    if len(w) != 1:
        return False
    r, c = w[0]
    return r == 0 and c != 3

def fires(b):
    return bottom_block(b)

def level(b):
    if b.my_playable_wins or len(b.their_playable_wins) >= 2:
        return 0
    if bottom_block(b):
        return 9
    if b.their_playable_wins:
        return 2
    n = 0
    for c in b.legal:
        r = b.landing(c)
        if (r + 1, c) in b.their_wins and (r + 1, c) not in b.my_wins:
            n += 1
    if n >= 2:
        return 7
    if n == 1:
        return 5
    return 0
