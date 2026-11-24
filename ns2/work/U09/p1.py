def score(b):
    g = b.grid[0]
    them = {0: 0.0, 1: 3.0, 2: 1.0, 3: 0.0, 4: 2.0, 5: 3.0, 6: 0.0}
    mine = {0: 0.0, 1: 0.0, 2: 1.0, 3: 2.0, 4: 0.0, 5: 0.0, 6: 1.5}
    s = 0.0
    for c in range(7):
        if g[c] == 2:
            s += them[c]
        elif g[c] == 1:
            s += mine[c]
    return s

def fires(b):
    return score(b) >= 9.0

def level(b):
    s = score(b)
    if s < 7.0:
        return 0
    return max(0, min(9, int((s - 7.0) * 2)))
