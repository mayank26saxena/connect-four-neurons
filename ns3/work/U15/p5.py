def col6_block(b):
    # an opponent winning cell sits on top of column 6 (column 6 not empty)
    return any(c == 6 and r >= 1 for (r, c) in b.their_playable_wins)

def col0_vthree(b):
    # opponent just made three stacked in column 0 with room above
    h = b.heights[0]
    if b.last_col != 0 or h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][0] == 2 for k in range(3))

def fires(b):
    return col6_block(b) or col0_vthree(b)

def level(b):
    if col6_block(b):
        return 8 if len(b.their_playable_wins) == 1 else 6
    if col0_vthree(b):
        return 6
    if b.their_playable_wins:
        return 3
    return 0
