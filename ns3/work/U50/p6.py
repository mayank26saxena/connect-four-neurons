def col6_mine(b):
    mine = [r for (r, c) in b.my_wins if c == 6]
    theirs = [r for (r, c) in b.their_wins if c == 6]
    return len(mine) > 0 and len(theirs) == 0

def lost(b):
    return len(b.their_playable_wins) >= 2

def fires(b):
    return col6_mine(b) or lost(b)

def level(b):
    if col6_mine(b):
        r3 = any(b.grid[r][3] == 1 and b.grid[r][4] == 1 and b.grid[r][5] == 1 for (r, c) in b.my_wins if c == 6)
        return 9 if r3 else 7
    if lost(b):
        return 6
    return 0
