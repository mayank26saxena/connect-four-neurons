def score(b):
    g = b.grid
    s = 0
    # opponent stones in center columns 3-4, low rows
    for c in (3, 4):
        for r in range(3):
            if g[r][c] == 2:
                s += 1
            elif g[r][c] == 1:
                s -= 1
    if g[0][2] == 1:
        s += 1
    if b.ply > 16:
        s -= 2
    return s

def fires(b):
    return score(b) >= 3

def level(b):
    return max(0, min(9, 2 * score(b) - 2))
