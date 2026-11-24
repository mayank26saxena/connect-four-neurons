W = [1.0, 1.5, 1.0, 0.7, -1.5, -0.5, 0.7]

def score(b):
    h = b.heights
    if h[4] == 6 and h[5] == 6:
        return 0.0
    return sum(W[c] * h[c] for c in range(7))

def level(b):
    s = score(b)
    if len(b.their_playable_wins) >= 2:
        s = max(s, 18.0)
    return max(0, min(9, int((s - 8) / 2)))

def fires(b):
    return level(b) >= 4
