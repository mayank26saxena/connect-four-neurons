def vert3(b):
    h = b.heights[0]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][0] == 2 for k in range(3))

def col0_cells(s):
    return [r for (r, c) in s if c == 0]

def fires(b):
    return level(b) >= 4

def level(b):
    if vert3(b):
        return 9
    if col0_cells(b.their_playable_wins):
        return 6
    if col0_cells(b.my_playable_wins):
        return 5
    if 3 in col0_cells(b.my_wins) or 3 in col0_cells(b.their_wins):
        return 4
    if b.last_col == 0 and b.last_row == 2:
        return 4
    if b.last_col == 0 and b.last_row == 1:
        return 2
    if b.heights[0] == 3:
        return 1
    return 0
