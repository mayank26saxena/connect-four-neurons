def bad_frac(b):
    if len(b.my_playable_wins) > 0:
        return 0.0
    mb = set(c for (r, c) in b.their_playable_wins)
    bad = 0
    for c in b.legal:
        r = b.landing(c)
        if len(mb) >= 2 or (len(mb) == 1 and c not in mb) or (r + 1, c) in b.their_wins:
            bad += 1
    return bad / max(1, len(b.legal))

def fires(b):
    return b.heights[4] == 6 and bad_frac(b) >= 0.5

def level(b):
    if b.heights[4] != 6:
        return 0
    return min(9, 2 + int(round(7 * bad_frac(b))))
