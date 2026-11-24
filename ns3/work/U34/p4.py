def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return len(b.their_playable_wins) > 0

def level(b):
    if vthree(b, 5):
        return 9 if b.last_col == 5 else 7
    if any(vthree(b, c) for c in (1, 6)):
        return 4
    if any(vthree(b, c) for c in (0, 2, 4)):
        return 3
    if b.their_playable_wins:
        return 2
    return 0
