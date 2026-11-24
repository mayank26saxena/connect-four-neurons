def their_vstack(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return their_vstack(b, 4) or their_vstack(b, 0) or their_vstack(b, 6)

def level(b):
    if their_vstack(b, 4):
        return 9
    if their_vstack(b, 0) or their_vstack(b, 6):
        return 3
    if their_vstack(b, 2):
        return 1
    return 0
