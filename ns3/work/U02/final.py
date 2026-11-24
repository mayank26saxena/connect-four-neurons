def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r < 5 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def core(b):
    return b.heights[0] == 6 and b.heights[3] == 6

def hopeless(b):
    if b.my_playable_wins:
        return False
    return len(poisoned(b)) > 0 or len(b.legal) == 1 or len(b.my_wins) == 0

def fires(b):
    return core(b) and nfull(b) >= 3 and hopeless(b)

def level(b):
    f = nfull(b)
    if not core(b):
        return min(2, f // 2)
    p = len(poisoned(b))
    s = f + 2 * p
    if p > 0 and p == len(b.legal):
        s += 2
    if b.my_playable_wins:
        s -= 4
    return max(0, min(9, s))
