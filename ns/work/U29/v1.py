def fires(b):
    if b.last_col != 3 or b.last_row < 1:
        return False
    mine = sum(1 for r in range(b.last_row) if b.grid[r][3] == 1)
    return mine >= 1 and b.ply >= 12

def level(b):
    if b.last_col != 3 or b.last_row < 1:
        return 0
    mine = sum(1 for r in range(b.last_row) if b.grid[r][3] == 1)
    if mine == 0:
        return 2
    s = 0.1 * (b.ply - 12) + 0.3 * mine + 0.8
    return max(0, min(9, int(round(s * 4))))
