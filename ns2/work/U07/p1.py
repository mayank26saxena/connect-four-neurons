def vert3(b):
    h = b.heights[3]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][3] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    return any(c == 3 for (r, c) in b.their_playable_wins)

def level(b):
    if b.my_playable_wins:
        return 0
    if vert3(b):
        return 9 if b.last_col == 3 else 5
    if any(c == 3 for (r, c) in b.their_playable_wins):
        return 5
    return 0
