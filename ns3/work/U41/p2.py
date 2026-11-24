def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def col1_block(b):
    r = b.landing(1)
    return r is not None and r >= 1 and (r, 1) in b.their_playable_wins

def level(b):
    if len(b.my_playable_wins) > 0 or not col1_block(b):
        return 0
    n = len(b.their_playable_wins)
    if vert3(b, 1):
        return 9 if n == 1 else 5
    return 6 if n == 1 else 0

def fires(b):
    return level(b) > 0
