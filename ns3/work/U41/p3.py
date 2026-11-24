def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def level(b):
    r = b.landing(1)
    if r is None:
        return 0
    if any(c != 1 for (rr, c) in b.my_playable_wins):
        return 0
    n = len(b.their_playable_wins)
    if (r, 1) in b.their_playable_wins and r >= 1:
        if vert3(b, 1):
            return 9 if n == 1 else 5
        return 6 if n == 1 else 0
    if n == 0 and (r + 1, 1) in b.their_wins:
        return 3
    return 0

def fires(b):
    return level(b) > 0
