def vert6(b):
    h = b.heights[6]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][6] == 2 for k in range(3))

def low_threat6(b):
    # opponent threat cell at the landing cell of column 6 (just set up by their stone in col 6)
    # or the cell directly above the landing cell
    r = b.landing(6)
    if r is None:
        return False
    if (r, 6) in b.their_wins and b.last_col == 6:
        return True
    if (r + 1, 6) in b.their_wins and not b.their_playable_wins:
        return True
    return False

def fires(b):
    return vert6(b) or low_threat6(b)

def level(b):
    if vert6(b):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if low_threat6(b):
        return 3
    return 0
