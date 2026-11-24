def bad_cols(b):
    if b.my_playable_wins:
        return 0
    blocks = set(c for (r, c) in b.their_playable_wins)
    bad = set()
    for c in b.legal:
        r = b.landing(c)
        if blocks and c not in blocks:
            bad.add(c)
        elif len(blocks) > 1:
            bad.add(c)
        elif (r + 1, c) in b.their_wins:
            bad.add(c)
    return len(bad)

def fires(b):
    return bad_cols(b) >= 4

def level(b):
    n = bad_cols(b)
    return [0, 1, 2, 3, 6, 8, 9, 9][n]
