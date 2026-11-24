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
    if b.heights[4] != 6 or len(b.their_wins) == 0:
        return False
    return bad_frac(b) >= 0.5 or len(b.their_wins) > len(b.my_wins)

def level(b):
    if b.heights[4] != 6:
        return 0
    s = 2 + 3 * bad_frac(b) + min(3, len(b.their_wins)) - 0.5 * min(2, len(b.my_wins))
    if len(b.my_playable_wins) > 0:
        s -= 1
    return max(1, min(9, int(round(s))))
