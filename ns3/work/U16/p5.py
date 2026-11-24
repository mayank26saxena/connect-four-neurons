def vertical_block(b, c):
    h = b.heights[c]
    return 3 <= h <= 5 and all(b.grid[h - 1 - k][c] == 2 for k in range(3))


def left_block(b):
    # I must block the opponent in column 1 or 2 (any line)
    return any(c in (1,) for (r, c) in b.their_playable_wins)


def under_own_threat(b):
    # opponent's last stone sits directly under a cell that completes their (non-vertical) line
    if b.last_col is None:
        return False
    cell = (b.last_row + 1, b.last_col)
    return cell in b.their_playable_wins and not vertical_block(b, b.last_col)


def edge_vertical(b):
    return vertical_block(b, 6) or vertical_block(b, 0) or vertical_block(b, 5)


def cap2(b):
    return b.grid[0][2] == 1 and b.grid[1][2] == 2 and b.heights[2] == 2


def fires(b):
    return left_block(b) or edge_vertical(b) or (cap2(b) and b.heights[3] == 0)


def level(b):
    s = 0
    if left_block(b):
        s += 5
        if under_own_threat(b):
            s += 3
    if edge_vertical(b):
        s += 4
    if cap2(b):
        s += 3
        if b.heights[3] == 0:
            s += 2
    return min(9, s)
