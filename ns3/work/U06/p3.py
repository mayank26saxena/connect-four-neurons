def fires(b):
    # opponent's last stone went into column 5 and the cell directly above it is now a must-block
    if b.last_col != 5 or len(b.my_playable_wins) > 0:
        return False
    r = b.landing(5)
    return r is not None and (r, 5) in b.their_playable_wins

def level(b):
    if not fires(b):
        return 1
    h = b.heights[5]
    vert = h >= 3 and all(b.grid[h - 1 - k][5] == 2 for k in range(3))
    return 9 if vert else 7
