def bad_cols(b):
    n = 0
    for c in range(6):
        if b.heights[c] == 5:
            n += 1
    if b.heights[6] in (2, 3, 4):
        n += 1
    return n

def soft(b):
    # weaker height dislikes seen in firing positions
    h = b.heights
    s = 0
    s += h[3] in (1, 3)
    s += h[2] == 2
    s += h[4] == 2
    s += h[0] in (3, 4)
    s += h[1] == 4
    s += h[5] == 4
    return s

def fires(b):
    return bad_cols(b) == 0 and soft(b) <= 1 and not b.my_playable_wins and not b.their_playable_wins

def level(b):
    if bad_cols(b) > 0:
        return 0
    s = soft(b)
    quiet = not b.my_playable_wins and not b.their_playable_wins
    base = [6, 3, 1, 0, 0, 0, 0][s]
    return base if quiet else base // 2
