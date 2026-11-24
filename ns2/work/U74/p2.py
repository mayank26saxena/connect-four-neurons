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
    if len(b.legal) < 2:
        return 0
    if len(b.their_playable_wins) >= 2:
        return 9
    if len(b.my_playable_wins) >= 2:
        return 4
    if len(b.my_playable_wins) > 0:
        return 0
    for c, v in ((2, 7), (4, 7), (3, 5)):
        if vert_threat(b, 2, c):
            return v
    if len(b.their_playable_wins) == 1:
        c = list(b.their_playable_wins)[0][1]
        return 3 if c in (2, 3, 4) else 1
    return 0
