def fires(b):
    h = b.heights
    if b.my_playable_wins:
        return False
    if h[1] == 2 and h[0] < 2:
        if b.grid[0][1] == 2 and b.grid[1][1] == 1:
            return False
        return h[2] >= 1 and h[3] >= 2
    if h[1] == 1 and h[0] == 0:
        return h[2] >= 1 and h[3] >= 2
    return False

def level(b):
    if not fires(b):
        return 0
    return 6 if b.heights[1] == 2 else 4
