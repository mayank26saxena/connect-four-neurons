LINE = [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]

def best(b):
    top = 0
    for s in range(2):
        w = LINE[s:s + 4]
        mine = sum(1 for (r, c) in w if b.grid[r][c] == 1)
        theirs = sum(1 for (r, c) in w if b.grid[r][c] == 2)
        if theirs == 0 and mine > top:
            top = mine
    return top

def fires(b):
    return best(b) >= 2 and len(b.my_playable_wins) == 0

def level(b):
    k = best(b)
    if len(b.my_playable_wins) > 0:
        return 1
    if k >= 3:
        return 7
    if k == 2:
        return 6
    return 0
