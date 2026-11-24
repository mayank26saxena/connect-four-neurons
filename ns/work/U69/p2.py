def good_rows(b):
    # row index parity that the opponent (last mover) gets in a fill-up endgame
    return 1 if b.me_first else 0

def their_good(b):
    p = good_rows(b)
    return [(r, c) for (r, c) in b.their_wins if r % 2 == p and r > b.heights[c]]

def fires(b):
    return len(their_good(b)) > 0

def level(b):
    n = len(their_good(b))
    if n == 0:
        return 0
    return min(9, 3 + 2 * n)
