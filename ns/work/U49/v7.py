HOT = {(2, 1): 3, (3, 1): 3, (3, 4): 3, (3, 0): 1, (1, 0): 1, (3, 5): 1, (4, 5): 1, (4, 3): 1, (4, 4): 1, (3, 6): 1, (4, 6): 1}

def forced_col(b):
    # the one sensible move: a single must-block, or the only column that does not hand them a win
    if b.my_playable_wins:
        return None
    mb = set(c for (r, c) in b.their_playable_wins)
    if len(mb) == 1:
        return list(mb)[0]
    if mb:
        return None
    safe = [c for c in b.legal if (b.landing(c) + 1, c) not in b.their_wins]
    if len(safe) == 1:
        return safe[0]
    return None

def score_pts(b):
    s = 0
    if b.last_col is not None:
        s += HOT.get((b.last_row, b.last_col), 0)
    f = forced_col(b)
    if f is not None:
        s += 2
        if f in (1, 4):
            s += 2
        if f == b.last_col:
            s += 1
    return s

def fires(b):
    return score_pts(b) >= 6

def level(b):
    return min(9, score_pts(b))
