def vert1(b):
    h = b.heights[1]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][1] == 2 for k in range(3))

def fires(b):
    if vert1(b):
        return True
    return any(c == 1 for (r, c) in b.their_playable_wins)

def level(b):
    if vert1(b):
        return 9
    if any(c == 1 for (r, c) in b.their_playable_wins):
        return 3
    return 0
