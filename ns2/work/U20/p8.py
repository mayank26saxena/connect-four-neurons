def vert_block(b):
    # opponent's vertical three in column 4 or 5 that I must block on top
    for (r, c) in b.their_playable_wins:
        if c in (4, 5) and r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3)):
            return True
    return False

def late(b):
    # endgame: column 4 full, right side (5, 6) full or nearly full, columns 1 and 2 still open
    h = b.heights
    return h[4] == 6 and (h[5] == 6 or h[5] + h[6] >= 10) and h[1] < 6 and h[2] < 6

def fires(b):
    return late(b) or vert_block(b)

def level(b):
    h = b.heights
    if vert_block(b):
        return 6
    if h[4] < 6:
        return 0
    s = 1 + max(0, h[5] + h[6] - 7)
    if h[5] == 6:
        s += 1
    if h[1] < 6 and h[2] < 6:
        s += 2
    if h[3] == 6:
        s += 1
    if h[0] == 6:
        s += 1
    return min(9, s)
