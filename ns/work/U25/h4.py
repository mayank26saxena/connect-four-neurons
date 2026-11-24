def losing_moves(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        lose = False
        for (wr, wc) in b.their_playable_wins:
            if not (wr == r and wc == c):
                lose = True
        if (r + 1, c) in b.their_wins:
            lose = True
        out.append(lose)
    return out

def fires(b):
    if len(b.my_playable_wins) > 0:
        return False
    lm = losing_moves(b)
    return len(lm) > 0 and all(lm)

def level(b):
    if len(b.my_playable_wins) > 0:
        return 1
    lm = losing_moves(b)
    if len(lm) == 0:
        return 0
    k = sum(1 for x in lm if x)
    if k == len(lm):
        return 9 if len(lm) <= 2 else 7
    if k == 0:
        return 0
    return 2 + (3 * k) // len(lm)
