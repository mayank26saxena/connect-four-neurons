def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return len(b.their_playable_wins) > 0

def level(b):
    if vthree(b, 0):
        return 9
    if b.their_playable_wins:
        return 5
    return 0
