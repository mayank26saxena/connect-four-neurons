def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return len(b.their_playable_wins) > 0

def level(b):
    if not fires(b):
        return 0
    cols = set(c for (r, c) in b.their_playable_wins)
    if vert3(b, 3):
        return 9
    if 3 in cols:
        return 6
    if any(vert3(b, c) for c in cols):
        return 4
    return 3
