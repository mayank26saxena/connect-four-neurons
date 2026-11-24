def stacked_cols(b, wins):
    # columns where two vertically adjacent empty cells (at or above the landing cell) both win for one side
    out = []
    for c in range(7):
        lr = b.landing(c)
        if lr is None:
            continue
        for r in range(lr, 5):
            if (r, c) in wins and (r + 1, c) in wins:
                out.append((r - lr, c))
                break
    return out

def fires(b):
    return level(b) >= 5

def level(b):
    mw = b.my_playable_wins
    tw = b.their_playable_wins
    st = stacked_cols(b, b.my_wins)
    if len(mw) >= 1 and any(d == 0 for d, c in st):
        return 9
    if len(mw) >= 2:
        return 8
    if len(tw) == 0 and len(st) > 0:
        return 7
    if len(mw) == 0 and len(tw) >= 2:
        return 5
    if len(mw) == 1:
        return 3
    return 0
