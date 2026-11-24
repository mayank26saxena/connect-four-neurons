WM = [-1.0, -0.3, 0.0, 0.0, -0.5, 1.0, 0.5]
WT = [0.5, -0.3, 0.5, -1.0, -0.5, 0.0, 0.0]
LB = {3: 3.0, 2: 1.5, 1: 2.0}

def score_b(b):
    mv = b.moves
    n = len(mv)
    s = LB.get(mv[-1], 0.0) + 0.2 * n
    for i in range(n - 1):
        c = mv[i]
        if (n - 1 - i) % 2 == 0:
            s += WT[c]
        else:
            s += WM[c]
    return s

def score_a(b):
    # short-game mode: me in column 0, them in columns 3/4, last move not in 2/3
    mv = b.moves
    n = len(mv)
    if n > 9 or mv[-1] in (2, 3):
        return -99.0
    s = {1: 2.0, 5: 1.0, 6: 1.0}.get(mv[-1], 0.0)
    for i in range(n - 1):
        c = mv[i]
        if (n - 1 - i) % 2 == 0:
            s += {3: 1.5, 4: 1.2, 6: 0.5, 2: -1.0}.get(c, 0.0)
        else:
            s += {0: 2.0, 5: -2.0, 6: -1.0}.get(c, 0.0)
    return s

def fires(b):
    if not b.moves:
        return False
    return score_b(b) >= 6.5 or score_a(b) >= 3.5

def level(b):
    if not b.moves:
        return 0
    s = max(score_b(b) - 6.5, score_a(b) - 3.5)
    return max(0, min(9, int(round(s + 4))))
