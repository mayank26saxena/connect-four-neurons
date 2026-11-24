def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def level(b):
    r = b.landing(1)
    if r is None or r < 1:
        return 0
    if len(b.my_playable_wins) > 0 or (r, 1) not in b.their_playable_wins:
        return 0
    n = len(b.their_playable_wins)
    if vert3(b, 1):
        return 9 if n == 1 else 5
    if n == 1 and r <= 3 and (r + 1, 1) not in b.their_wins:
        return 6
    return 0

def fires(b):
    return level(b) > 0
