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

def fires(b):
    return base(b) and len(poisoned(b)) > 0 and len(b.my_playable_wins) == 0

def level(b):
    f = nfull(b)
    p = len(poisoned(b))
    if not (b.heights[0] == 6 and b.heights[3] == 6):
        return min(2, f // 2)
    s = f - 1 + 2 * p
    if b.my_playable_wins:
        s -= 3
    return max(0, min(9, s))
