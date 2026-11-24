def score(b):
    g = b.grid
    s = 0.0
    if g[0][4] == 2: s += 2.0
    if g[1][3] == 2: s += 1.2
    if g[2][2] == 2: s += 1.2
    if g[0][3] == 2: s += 1.0
    if g[0][0] == 2: s += 0.5
    if g[0][5] == 1: s += 0.5
    if g[0][4] == 1: s -= 1.5
    if (3, 1) in b.their_wins: s += 1.5
    s -= 0.7 * sum(1 for r in range(6) if g[r][1] == 1)
    if b.their_playable_wins: s -= 2.0
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 1.5:
        return 0
    return max(0, min(9, int((s - 1.5) * 2)))
