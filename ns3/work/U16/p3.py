def block_on_last(b):
    # the cell I must block is directly on top of the opponent's last stone
    if b.last_col is None:
        return False
    return (b.last_row + 1, b.last_col) in b.their_playable_wins


def cap2(b):
    # my stone at the bottom of column 2 capped by theirs, nothing above
    return b.grid[0][2] == 1 and b.grid[1][2] == 2 and b.heights[2] == 2


def fires(b):
    return block_on_last(b) or cap2(b)


def level(b):
    s = 0
    if block_on_last(b):
        s += 6
    if cap2(b):
        s += 5
        if b.heights[3] == 0:
            s += 2
    return min(9, s)
