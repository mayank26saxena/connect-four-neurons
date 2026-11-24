def fires(b):
    return any(c == 5 for (r, c) in b.their_playable_wins)

def level(b):
    if not fires(b):
        return 0
    if b.heights[5] == 3 and all(b.grid[r][5] == 2 for r in range(3)):
        return 9
    return 6
