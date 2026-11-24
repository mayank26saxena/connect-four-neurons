def vertical_block(b):
    # columns where the opponent has three stacked on top with the cell above empty (a vertical must-block)
    out = []
    for c in range(7):
        h = b.heights[c]
        if 3 <= h <= 5 and all(b.grid[h - 1 - k][c] == 2 for k in range(3)):
            out.append(c)
    return out


def pat_a(b):
    return any(c in (0, 1, 5, 6) for c in vertical_block(b))


def pat_b(b):
    return (1, 1) in b.their_playable_wins


def pat_c(b):
    return b.grid[0][2] == 1 and b.grid[1][2] == 2 and b.heights[2] == 2 and b.heights[3] == 0


def fires(b):
    return pat_a(b) or pat_b(b) or pat_c(b)


def level(b):
    s = 0
    if pat_a(b):
        s += 5
    if pat_b(b):
        s += 6
    if pat_c(b):
        s += 6
    return min(9, s)
