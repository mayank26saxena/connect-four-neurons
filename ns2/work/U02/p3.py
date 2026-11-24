def col3_all_theirs(b):
    h = b.heights[3]
    return h > 0 and all(b.grid[r][3] == 2 for r in range(h))

def fires(b):
    return b.last_col == 3 and col3_all_theirs(b) and b.ply >= 9

def level(b):
    if b.last_col != 3 or not col3_all_theirs(b):
        return 0
    s = b.ply + b.heights[2] + b.heights[4] - 3 * b.last_row
    if s >= 20:
        return 9
    if s >= 15:
        return 7
    if s >= 11:
        return 5
    if s >= 8:
        return 3
    return 1
