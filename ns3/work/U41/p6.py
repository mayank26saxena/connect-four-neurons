def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def level(b):
    if len(b.my_playable_wins) > 0:
        return 0
    n = len(b.their_playable_wins)
    r = b.landing(1)
    if r is not None and r >= 1 and (r, 1) in b.their_playable_wins:
        if vert3(b, 1):
            return 9 if n == 1 else 5
        if n == 1 and r <= 3 and (r + 1, 1) not in b.their_wins:
            return 6
        return 0
    if n == 1:
        for c in (0, 2):
            rc = b.landing(c)
            if rc is not None and rc >= 1 and (rc, c) in b.their_playable_wins and (rc + 1, c) not in b.their_wins:
                return 2
    return 0

def fires(b):
    return level(b) > 0
