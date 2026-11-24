def vert_block(b):
    for (r, c) in b.their_playable_wins:
        if c in (3, 4, 5) and r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3)):
            return True
    return False

def late(b):
    return b.heights[4] == 6 and b.heights[5] == 6 and b.heights[1] < 6 and b.heights[2] < 6

def fires(b):
    return late(b) or vert_block(b)

def level(b):
    if vert_block(b):
        return 6
    if b.heights[4] < 6:
        return 0
    s = 2
    if b.heights[5] == 6:
        s += 2
    if b.heights[1] < 6 and b.heights[2] < 6:
        s += 2
    if b.heights[3] == 6 or b.heights[6] == 6:
        s += 1
    if b.heights[0] == 6:
        s += 1
    if b.ply % 2 == 1:
        s += 1
    return min(9, s)
