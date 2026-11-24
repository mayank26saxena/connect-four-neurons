def score(b):
    h = b.heights
    h0 = h[0]
    if h0 == 6:
        return 0
    if b.my_playable_wins or b.their_playable_wins:
        return 1
    tall = sum(1 for c in range(7) if h[c] >= 5)
    low = sum(1 for c in range(7) if h[c] <= 1)
    s = 0
    if h0 == 5:
        s += 3
    elif h0 <= 1:
        s += 1
    if tall >= 3:
        s += 2
    if tall >= 4:
        s += 1
    if 1 <= low <= 2:
        s += 1
    if 22 <= b.ply <= 35:
        s += 1
    return min(9, s)

def fires(b):
    return score(b) >= 7

def level(b):
    return score(b)
