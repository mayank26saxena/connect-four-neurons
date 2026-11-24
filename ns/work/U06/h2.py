def vert(b, r, c):
    return r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3))

def horiz0(b, r):
    return all(b.grid[r][k] == 2 for k in (1, 2, 3))

def kind(b):
    best = 0
    for (r, c) in b.their_playable_wins:
        if c == 0 and vert(b, r, 0):
            best = max(best, 3)
        elif c == 0 and horiz0(b, r):
            best = max(best, 2)
        elif c in (2, 5) and vert(b, r, c):
            best = max(best, 1)
    return best

def fires(b):
    return kind(b) > 0

def level(b):
    k = kind(b)
    if k == 0:
        return 0
    lv = {3: 9, 2: 6, 1: 4}[k]
    if b.my_playable_wins:
        lv -= 3
    return lv
