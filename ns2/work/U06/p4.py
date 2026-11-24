# per-stone weights (units of 0.001 activation) measured with single-stone substitutions
WM = [-0.56, -0.05, 0.02, 0.19, -0.30, 0.48, 0.28]
WT = [0.26, 0.09, 0.38, -0.43, -0.22, 0.18, -0.18]
LB = [-1.08, -0.13, 0.99, 1.32, -0.28, -0.21, -0.68]

def score_b(b):
    mv = b.moves
    n = len(mv)
    s = LB[mv[-1]]
    for i in range(n - 1):
        c = mv[i]
        if (n - 1 - i) % 2 == 0:
            s += WT[c]
        else:
            s += WM[c]
    return s

def score_a(b):
    # very short games: me in column 0, them in columns 3/4, last move not 2/3
    mv = b.moves
    n = len(mv)
    if n > 7 or mv[-1] in (2, 3):
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
    return score_b(b) >= 2.8 or score_a(b) >= 3.5

def level(b):
    if not b.moves:
        return 0
    s = max((score_b(b) - 0.8) * 2.5, (score_a(b) - 1.5) * 2.5)
    return max(0, min(9, int(round(s))))
