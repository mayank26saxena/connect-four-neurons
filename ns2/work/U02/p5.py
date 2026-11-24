def strength(b):
    # opponent just dropped into the centre column, which holds only their stones, low down
    if b.last_col != 3 or b.last_row > 1:
        return -1
    if any(b.grid[r][3] != 2 for r in range(b.heights[3])):
        return -1
    return b.ply + b.heights[2] + b.heights[4] - 6 * b.last_row

def fires(b):
    return strength(b) >= 12

def level(b):
    s = strength(b)
    if s >= 22:
        return 9
    if s >= 18:
        return 8
    if s >= 15:
        return 7
    if s >= 12:
        return 5
    if s >= 9:
        return 3
    if s >= 0:
        return 2
    if b.last_row == 0 and b.ply >= 12:
        return 2
    if b.heights[3] == 0:
        return 0
    return 1
