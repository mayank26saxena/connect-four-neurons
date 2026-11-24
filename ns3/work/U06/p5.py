def fires(b):
    # opponent threatens to win right now in column 5, at row 3 or higher
    if not all(c == 5 for (r, c) in b.my_playable_wins):
        return False
    return any(c == 5 and r >= 3 for (r, c) in b.their_playable_wins)

def level(b):
    if not fires(b):
        return 1
    h = b.heights[5]
    vert = h >= 3 and all(b.grid[h - 1 - k][5] == 2 for k in range(3))
    return 9 if vert else 7
