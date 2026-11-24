def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def fires(b):
    h0 = b.heights[0]
    if h0 == 6 or b.my_playable_wins or b.their_playable_wins:
        return False
    f = nfull(b)
    if h0 == 5:
        return f >= 2
    if h0 <= 1:
        return f >= 3
    return False

def level(b):
    h0 = b.heights[0]
    if h0 == 6:
        return 0
    if b.my_playable_wins or b.their_playable_wins:
        return 1
    f = nfull(b)
    if h0 == 5:
        return min(9, 4 + f)
    if h0 <= 1:
        return min(9, 1 + f)
    return 2
