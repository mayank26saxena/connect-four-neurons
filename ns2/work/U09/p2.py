def score(b):
    g = b.grid
    them = [0.0, 3.0, 1.0, 0.0, 2.0, 3.0, -0.5]
    mine = [0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 1.5]
    s = 0.0
    for c in range(7):
        if g[0][c] == 2:
            s += them[c]
        elif g[0][c] == 1:
            s += mine[c]
        for r in range(1, 6):
            v = g[r][c]
            if v == 2:
                s -= 0.3 if c == 3 else 1.0
            elif v == 1:
                if c == 3:
                    s += 0.8
                elif c == 4 or c == 5:
                    s -= 0.6
    return s

def fires(b):
    return score(b) >= 8.6

def level(b):
    s = score(b)
    if s < 7.5:
        return 0
    return max(0, min(9, int((s - 7.5) * 1.5)))
