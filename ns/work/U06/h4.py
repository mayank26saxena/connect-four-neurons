def vert(b, r, c):
    return r >= 3 and all(b.grid[r - k][c] == 2 for k in (1, 2, 3))

def horiz0(b, r):
    return all(b.grid[r][k] == 2 for k in (1, 2, 3))

def kind(b):
    blocks = b.their_playable_wins
    if blocks and not any(c != 0 for (r, c) in blocks):
        best = 0
        for (r, c) in blocks:
            if vert(b, r, 0):
                best = max(best, 3)
            elif horiz0(b, r):
                best = max(best, 2)
        return best
    if blocks:
        return 0
    # early opening: I have two stones stacked in column 4, column 4 not yet capped
    if b.ply <= 8 and b.heights[4] == 2 and b.grid[0][4] == 1 and b.grid[1][4] == 1 and b.heights[0] == 0:
        return 1
    return 0

def fires(b):
    return kind(b) > 0

def level(b):
    k = kind(b)
    if k == 0:
        return 0
    if k == 1:
        return 2
    lv = 8 if k == 3 else 5
    if b.my_playable_wins:
        lv -= 3
    if b.ply > 30:
        lv -= 2
    return lv
