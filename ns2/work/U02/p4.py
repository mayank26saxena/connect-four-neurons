def fires(b):
    return b.last_col == 3 and b.last_row == 0 and b.ply >= 9

def level(b):
    if b.last_col == 3 and b.last_row == 0:
        s = b.ply + b.heights[2] + b.heights[4]
        if s >= 20:
            return 9
        if s >= 16:
            return 8
        if s >= 12:
            return 6
        if s >= 9:
            return 4
        return 2
    if b.last_col == 3 and b.last_row == 1 and b.grid[0][3] == 2:
        return 3
    if b.last_row == 0 and b.ply >= 12:
        return 3
    if b.heights[3] >= 1 and b.heights[3] <= 2 and b.grid[0][3] == 2:
        return 2
    if b.heights[3] == 0:
        return 0
    return 1
