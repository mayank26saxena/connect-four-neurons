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
    return col2_threat(b) >= 6

def level(b):
    return col2_threat(b)
