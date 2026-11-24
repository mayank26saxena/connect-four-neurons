def col1_shape(b):
    h1 = b.heights[1]
    if h1 < 2 or h1 > 4:
        return False
    return b.grid[h1 - 1][1] == 2 and b.heights[2] >= 4 and b.heights[3] >= 5

def fires(b):
    return col1_shape(b) or (b.last_col == 4 and b.last_row == 3 and (4, 4) in b.their_playable_wins)

def level(b):
    if fires(b):
        return 8 if b.last_col in (1, 4) else 6
    s = 0
    if 2 <= b.heights[1] <= 4:
        s += 1
    if b.heights[2] >= 4:
        s += 1
    if b.heights[3] >= 5:
        s += 1
    return s
