def their_vstack(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return their_vstack(b, 4)

def level(b):
    return 9 if fires(b) else 0
