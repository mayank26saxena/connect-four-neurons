def vthree(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def weak(b):
    # opponent threat cell that is playable now, in columns 1, 2 or 5
    for (r, c) in b.their_playable_wins:
        if c in (1, 2, 5):
            return True
    return False

def fires(b):
    return vthree(b, 5, 2) or vthree(b, 5, 1) or weak(b)

def level(b):
    if vthree(b, 5, 2):
        return 9 if b.last_col == 5 else 6
    if vthree(b, 5, 1):
        return 3
    if weak(b):
        return 2
    return 0
