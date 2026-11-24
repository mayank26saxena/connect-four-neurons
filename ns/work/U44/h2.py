def open_twos(b, p):
    # horizontal pairs of player p in rows >= 1 with both flanking cells empty
    n = 0
    g = b.grid
    for r in range(1, 6):
        for c in range(1, 5):
            if g[r][c] == p and g[r][c + 1] == p and g[r][c - 1] == 0 and g[r][c + 2] == 0:
                n += 1
    return n

def score(b):
    return open_twos(b, 2) + open_twos(b, 1)

def fires(b):
    return score(b) >= 1

def level(b):
    return min(9, 4 * score(b))
