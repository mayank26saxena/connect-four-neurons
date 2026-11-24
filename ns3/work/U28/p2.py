def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def block0(b):
    return any(c == 0 for (r, c) in b.their_playable_wins)

def fires(b):
    return vert3(b, 0) or block0(b)

def level(b):
    if vert3(b, 0):
        return 9
    if block0(b):
        return 4
    return 0
