def vertical_block(b, c):
    h = b.heights[c]
    return 3 <= h <= 5 and all(b.grid[h - 1 - k][c] == 2 for k in range(3))


def col1_block(b):
    # I must block the opponent in column 1 (any line)
    return any(c == 1 for (r, c) in b.their_playable_wins)


def col6_vertical(b):
    return vertical_block(b, 6)


def cap2(b):
    return b.grid[0][2] == 1 and b.grid[1][2] == 2 and b.heights[2] == 2 and b.heights[3] == 0


def fires(b):
    return col1_block(b) or col6_vertical(b) or cap2(b)


def level(b):
    s = 0
    if col1_block(b):
        s += 6
        if (1, 1) in b.their_playable_wins:
            s += 2
    if col6_vertical(b):
        s += 5
    if cap2(b):
        s += 5
    return min(9, s)
