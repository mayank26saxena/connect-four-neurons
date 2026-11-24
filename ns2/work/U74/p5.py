def vert_threat(b, who, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def fires(b):
    if len(b.legal) < 2:
        return False
    if len(b.their_playable_wins) >= 2:
        return True
    if len(b.my_playable_wins) > 0:
        return False
    return any(vert_threat(b, 2, c) for c in (2, 3, 4))

def level(b):
    tw = b.their_playable_wins
    if len(b.legal) >= 2 and len(tw) >= 2:
        return 9
    if fires(b):
        if vert_threat(b, 2, 3):
            return 7 if b.heights[3] >= 4 else 6
        return 8
    if len(b.my_playable_wins) > 0:
        return 3
    if len(tw) == 1:
        c = list(tw)[0][1]
        if c in (5, 6):
            return 0
        if c in (0, 1):
            return 2
        return 4
    return 1
