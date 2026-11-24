def col5_block(b):
    return any(c == 5 for (r, c) in b.their_playable_wins)

def fires(b):
    # opponent threatens to win right now in column 5 (I must block there)
    if not col5_block(b):
        return False
    # an immediate win of my own elsewhere makes the block irrelevant
    return all(c == 5 for (r, c) in b.my_playable_wins)

def level(b):
    if not fires(b):
        return 1
    h = b.heights[5]
    vert = h >= 3 and all(b.grid[h - 1 - k][5] == 2 for k in range(3))
    return 9 if vert else 7
