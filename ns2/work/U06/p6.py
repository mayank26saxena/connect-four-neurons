# per-stone weights (units of 0.001 activation) measured with single-stone substitutions
WM = [-0.56, -0.05, 0.02, 0.19, -0.30, 0.48, 0.28]
WT = [0.26, 0.09, 0.38, -0.43, -0.22, 0.18, -0.18]
LB = [-1.08, -0.13, 0.99, 1.32, -0.28, -0.21, -0.68]
LA = [0.3, 1.0, -1.5, -1.5, 0.3, 0.3, 0.3]

def ctx(b):
    mv = b.moves
    n = len(mv)
    s = 0.0
    for i in range(n - 1):
        c = mv[i]
        if (n - 1 - i) % 2 == 0:
            s += WT[c]
        else:
            s += WM[c]
    return s

def fires(b):
    if not b.moves:
        return False
    x = ctx(b)
    L = b.moves[-1]
    return x + LB[L] >= 2.6 or (len(b.moves) <= 12 and -x + LA[L] >= 2.2)

def level(b):
    if not b.moves:
        return 0
    x = ctx(b)
    L = b.moves[-1]
    s = (x + LB[L] - 0.6) * 2.5
    if len(b.moves) <= 12:
        s = max(s, (-x + LA[L] - 0.2) * 2.5)
    return max(0, min(9, int(round(s))))
