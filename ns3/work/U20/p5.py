def col2_threat(b):
    best = 0
    for (r, c) in b.their_playable_wins:
        if c != 2:
            continue
        if r >= 3 and all(b.grid[r - k][2] == 2 for k in (1, 2, 3)):
            best = max(best, 9)
        elif r == 2:
            best = max(best, 6)
        else:
            best = max(best, 3)
    return best

def fires(b):
    if len(b.their_playable_wins) > 1:
        return False
    return col2_threat(b) >= 6

def level(b):
    t = col2_threat(b)
    if t >= 6 and len(b.their_playable_wins) > 1:
        t = 3
    if t == 0 and b.heights[2] == 2:
        t = 1
    return t
