def vert_threat(b, who, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def diag_through(b, who, r, c):
    for dr, dc in ((1, 1), (1, -1)):
        for s in range(-3, 1):
            ok = True
            for k in range(4):
                rr = r + (s + k) * dr
                cc = c + (s + k) * dc
                if rr < 0 or rr > 5 or cc < 0 or cc > 6:
                    ok = False
                    break
                if (rr, cc) != (r, c) and b.grid[rr][cc] != who:
                    ok = False
                    break
            if ok:
                return True
    return False

def fires(b):
    if len(b.legal) < 2:
        return False
    if len(b.their_playable_wins) >= 2:
        return True
    if len(b.my_playable_wins) > 0:
        return False
    if any(vert_threat(b, 2, c) for c in (2, 3, 4)):
        return True
    return any(c in (2, 3, 4) and diag_through(b, 2, r, c) for (r, c) in b.their_playable_wins)

def level(b):
    if len(b.legal) < 2:
        return 0
    if len(b.their_playable_wins) >= 2:
        return 9
    if len(b.my_playable_wins) > 0:
        return 0
    for c, v in ((2, 7), (4, 7), (3, 6)):
        if vert_threat(b, 2, c):
            return v
    if fires(b):
        return 5
    if len(b.their_playable_wins) == 1:
        return 2
    return 0
