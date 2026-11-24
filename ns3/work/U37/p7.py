def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def score(b):
    h0 = b.heights[0]
    if h0 == 6:
        return 0
    if b.my_playable_wins or b.their_playable_wins:
        return 1
    f = nfull(b)
    s = 2
    if h0 == 5 and f >= 2:
        s = 5 + min(f, 4)
    elif h0 <= 1 and f >= 3:
        s = 4 + min(f, 4)
    top = b.last_row is not None and b.last_row >= 4
    if top and f >= 2:
        s = max(s, 6) + 1
    return min(9, s)

def fires(b):
    return score(b) >= 7

def level(b):
    return score(b)
