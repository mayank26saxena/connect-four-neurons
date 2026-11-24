def fires(b):
    # center column holds exactly three stones and the top one (row 2) is the opponent's
    return b.heights[3] == 3 and b.grid[2][3] == 2

def level(b):
    if not fires(b):
        return 0
    if b.last_col == 3:
        return 8 if b.ply <= 10 else 6
    return 4
