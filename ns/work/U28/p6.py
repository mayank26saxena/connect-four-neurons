def vert3(b):
    h = b.heights[0]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][0] == 2 for k in range(3))

def col0_rows(s):
    return [r for (r, c) in s if c == 0]

def drop0(b):
    # opponent just made column 0 three stones tall, mid/late game, and playing on top is not suicidal
    return (b.last_col == 0 and b.last_row == 2 and b.ply >= 12
            and (4, 0) not in b.their_wins)

def fires(b):
    return level(b) >= 4

def level(b):
    h = b.heights[0]
    if vert3(b):
        return 9
    if col0_rows(b.their_playable_wins):
        return 6
    if drop0(b):
        return 4
    if b.last_col == 0 and b.last_row == 2:
        return 3
    if b.last_col == 0 and b.last_row == 1:
        return 2
    if h == 3:
        return 1
    return 0
