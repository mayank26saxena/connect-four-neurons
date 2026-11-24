def vert5(b):
    h = b.heights[5]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][5] == 2 for k in range(3))

def block5(b):
    return any(c == 5 for (r, c) in b.their_playable_wins)

def fires(b):
    if len(b.my_playable_wins) > 0:
        return False
    if len(b.their_playable_wins) > 1:
        return False
    return block5(b)

def level(b):
    if not fires(b):
        return 0
    if vert5(b):
        return 9 if b.last_col == 5 else 6
    return 5
