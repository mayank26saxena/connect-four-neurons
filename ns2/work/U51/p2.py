def good_threats(b):
    # opponent's threat cells on rows of the opponent's good parity
    par = 0 if not b.me_first else 1
    return [(r, c) for (r, c) in b.their_wins if r % 2 == par and (r, c) not in b.their_playable_wins]

def fires(b):
    return len(good_threats(b)) >= 1

def level(b):
    return min(9, 4 * len(good_threats(b)))
