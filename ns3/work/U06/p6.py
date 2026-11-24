def fires(b):
    # opponent threatens to win right now in column 5 (row 3+, or row 2 right above their last stone)
    if not all(c == 5 for (r, c) in b.my_playable_wins):
        return False
    for (r, c) in b.their_playable_wins:
        if c == 5 and (r >= 3 or (r == 2 and b.last_col == 5)):
            return True
    return False

def level(b):
    if fires(b):
        h = b.heights[5]
        vert = h >= 3 and all(b.grid[h - 1 - k][5] == 2 for k in range(3))
        return 9 if vert else 7
    # negative side: my own win threat in column 5
    if any(c == 5 for (r, c) in b.my_playable_wins):
        return 0
    return 1
