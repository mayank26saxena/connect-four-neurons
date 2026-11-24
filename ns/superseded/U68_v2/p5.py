def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def col0_block(b):
    # opponent's immediate winning cell is the landing cell of column 0, at row 2 or higher
    return any(c == 0 and r >= 2 for (r, c) in b.their_playable_wins)

def fires(b):
    return vthree(b, 0) or col0_block(b)

def level(b):
    if vthree(b, 0):
        return 9 if b.heights[1] <= 2 else 7
    if col0_block(b):
        return 5
    return 0
