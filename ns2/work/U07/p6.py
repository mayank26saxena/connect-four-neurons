def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    return vert3(b, 3) or len(b.their_playable_wins) >= 2

def level(b):
    if b.my_playable_wins:
        return 0
    if vert3(b, 3):
        return 9 if b.last_col == 3 else 6
    if len(b.their_playable_wins) >= 2:
        return 6
    if b.their_playable_wins:
        return 3
    return 0
