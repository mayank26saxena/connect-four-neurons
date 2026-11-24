LASTW = [-0.15, -0.25, -0.6, -0.6, -0.6, -0.4, 0.0]
W1 = [-0.13, -0.17, 0.0, 0.09, 0.2, -0.21, 0.06]
W2 = [0.10, 0.0, 0.0, 0.09, 0.2, -0.21, 0.06]

def score(b):
    p = b.ply
    if p < 28:
        return -1.0
    s = 1.22 + 0.15 * (p - 34)
    if p % 2 == 1:
        s -= 0.75
    m = b.moves
    for i in range(len(m) - 1):
        if i % 2 == 0:
            s += W1[m[i]]
        else:
            s += W2[m[i]]
    s += LASTW[m[-1]]
    return s

def fires(b):
    return score(b) > 1.167

def level(b):
    s = score(b)
    v = int((s - 0.2) / 0.25)
    return max(0, min(9, v))
