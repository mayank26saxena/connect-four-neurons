def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def col1_block(b):
    r = b.landing(1)
    return r is not None and r >= 1 and (r, 1) in b.their_playable_wins

def fires(b):
    return col1_block(b) or vert3(b, 2)

def level(b):
    n = len(b.their_playable_wins)
    if vert3(b, 1):
        return 9 if n == 1 else 5
    if col1_block(b):
        return 5 if n == 1 else 2
    if vert3(b, 2):
        return 3
    return 0
