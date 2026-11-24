def well(b):
    # deepest step from an empty column (1-4) up to a neighbouring column
    h = b.heights
    best = 0
    for c in range(1, 5):
        if h[c] == 0:
            best = max(best, h[c - 1], h[c + 1])
    return best

def fires(b):
    if b.ply < 5 or b.ply > 22:
        return False
    if b.my_playable_wins or b.their_playable_wins:
        return False
    w = well(b)
    return w >= 4 or (w >= 2 and b.heights[2] == 0 and b.heights[3] >= 2)

def level(b):
    if b.ply < 5 or b.ply > 22:
        return 0
    s = well(b)
    if b.heights[2] == 0:
        s += 2
    if b.my_playable_wins or b.their_playable_wins:
        s -= 3
    return max(0, min(9, s))
