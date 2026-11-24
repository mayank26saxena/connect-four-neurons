def vert(b, r, c):
    return r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3))

def horiz0(b, r):
    return all(b.grid[r][k] == 2 for k in (1, 2, 3))

def col0_block(b):
    # strength of the opponent's immediate threat in column 0: 3 vertical, 2 horizontal, 1 other (diagonal), 0 none
    best = 0
    for (r, c) in b.their_playable_wins:
        if c != 0:
            continue
        if vert(b, r, 0):
            best = max(best, 3)
        elif horiz0(b, r):
            best = max(best, 2)
        else:
            best = max(best, 1)
    return best

def fires(b):
    return col0_block(b) > 0

def level(b):
    k = col0_block(b)
    if k == 0:
        return 0
    lv = {3: 9, 2: 6, 1: 4}[k]
    if any(c != 0 for (r, c) in b.their_playable_wins):
        lv -= 3
    if b.my_playable_wins:
        lv -= 2
    if b.ply > 30:
        lv -= 2
    return max(lv, 1)
