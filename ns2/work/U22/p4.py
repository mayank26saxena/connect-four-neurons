def poisoned(b):
    out = []
    for c in b.legal:
        r = b.landing(c)
        if r is not None and r + 1 <= 5 and (r + 1, c) in b.their_wins:
            out.append(c)
    return out

def fires(b):
    g = b.grid
    if g[3][3] == 1:
        return False
    return len(poisoned(b)) > 0 and (g[3][3] == 2 or g[2][4] == 2)

def level(b):
    return 6 if fires(b) else 0
