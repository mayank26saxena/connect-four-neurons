def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def col3_block(b):
    return any(c == 3 for (r, c) in b.their_playable_wins)

def fires(b):
    if b.my_playable_wins or b.ply > 28:
        return False
    if col3_block(b):
        return True
    c = b.last_col
    return c in (1, 2) and vert3(b, c)

def level(b):
    if b.my_playable_wins or b.ply > 28:
        return 0
    if col3_block(b):
        if b.last_col == 3 and vert3(b, 3):
            return 9
        return 7
    c = b.last_col
    if c in (1, 2) and vert3(b, c):
        return 6
    return 0
