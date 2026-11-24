def fires(b):
    h = b.heights
    if b.my_playable_wins or b.their_playable_wins:
        return False
    if h[1] not in (1, 2, 5) or h[0] >= h[1] or h[2] == 0:
        return False
    if h[1] == 2 and b.grid[0][1] == 2 and b.grid[1][1] == 1:
        return False
    return h[3] >= 2

def level(b):
    if not fires(b):
        return 0
    return {1: 4, 2: 6, 5: 3}[b.heights[1]]
