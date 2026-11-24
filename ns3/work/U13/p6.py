def vert6(b):
    h = b.heights[6]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][6] == 2 for k in range(3))

def near_threat6(b):
    # opponent just played in column 6 and has a threat cell at the new landing cell or right above it
    if b.last_col != 6:
        return False
    r = b.landing(6)
    if r is None:
        return False
    return (r, 6) in b.their_wins or (r + 1, 6) in b.their_wins

def fires(b):
    return vert6(b) or near_threat6(b)

def level(b):
    if vert6(b):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if near_threat6(b):
        return 3
    return 0
