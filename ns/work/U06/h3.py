def vert(b, r, c):
    return r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3))

def horiz0(b, r):
    return all(b.grid[r][k] == 2 for k in (1, 2, 3))

def kind(b):
    blocks = b.their_playable_wins
    if any(c != 0 for (r, c) in blocks):
        return 0
    best = 0
    for (r, c) in blocks:
        if vert(b, r, 0):
            best = max(best, 2)
        elif horiz0(b, r):
            best = max(best, 1)
    return best

def fires(b):
    return kind(b) > 0

def level(b):
    k = kind(b)
    if k == 0:
        return 0
    lv = 8 if k == 2 else 5
    if b.my_playable_wins:
        lv -= 3
    if b.ply > 30:
        lv -= 2
    return lv
