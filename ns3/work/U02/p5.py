def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r < 5 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def base(b):
    return b.heights[0] == 6 and b.heights[3] == 6 and nfull(b) >= 4

def hopeless(b):
    # no immediate win, and either a column is poisoned, only one move is left, or I have no threats at all
    if b.my_playable_wins:
        return False
    return len(poisoned(b)) > 0 or len(b.legal) == 1 or len(b.my_wins) == 0

def fires(b):
    return base(b) and hopeless(b)

def level(b):
    f = nfull(b)
    if not (b.heights[0] == 6 and b.heights[3] == 6):
        return min(2, f // 2)
    s = f - 1
    if hopeless(b):
        s += 2 + 2 * len(poisoned(b))
    elif b.my_playable_wins:
        s -= 2
    return max(0, min(9, s))
