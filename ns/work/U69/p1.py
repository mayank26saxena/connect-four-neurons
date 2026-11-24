def stacked(b):
    n = 0
    for (r, c) in b.their_wins:
        if (r + 1, c) in b.their_wins:
            n += 1
    return n

def fires(b):
    return stacked(b) > 0

def level(b):
    n = stacked(b)
    if n == 0:
        return 0
    return min(9, 4 + 2 * n + (1 if b.ply >= 30 else 0))
