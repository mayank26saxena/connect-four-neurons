def vert3(b):
    h = b.heights[0]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][0] == 2 for k in range(3))

def col0_block(b):
    return any(c == 0 for (r, c) in b.their_playable_wins)

def fires(b):
    return vert3(b) or col0_block(b)

def level(b):
    if vert3(b):
        return 9
    if col0_block(b):
        return 6
    return 0
