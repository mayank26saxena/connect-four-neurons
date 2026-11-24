def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    c = b.last_col
    return c is not None and c in (1, 2, 3) and vert3(b, c)

def level(b):
    if b.my_playable_wins:
        return 0
    c = b.last_col
    if c is None:
        return 0
    if c == 3 and vert3(b, 3):
        return 9
    if c in (1, 2) and vert3(b, c):
        return 5
    if vert3(b, 3):
        return 3
    return 0
