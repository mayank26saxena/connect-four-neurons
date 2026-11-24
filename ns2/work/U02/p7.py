def opened_centre(b):
    # opponent's last move went into column 3, low (row 0 or 1), and column 3 holds only their stones
    if b.last_col != 3 or b.last_row > 1:
        return False
    return all(b.grid[r][3] == 2 for r in range(b.heights[3]))

def fires(b):
    if not opened_centre(b):
        return False
    return b.ply >= (9 if b.last_row == 0 else 13)

def level(b):
    if opened_centre(b):
        if b.last_row == 1:
            return 5 if b.ply >= 13 else 3
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
    if b.last_col == 3 and b.grid[0][3] == 2 and b.heights[3] <= 3:
        return 2
    if b.last_row == 0 and b.ply >= 12:
        return 2
    if b.heights[3] == 0:
        return 0
    return 1
