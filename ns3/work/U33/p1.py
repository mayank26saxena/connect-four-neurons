def _mine_below(b):
    return sum(1 for r in range(b.heights[5]) if b.grid[r][5] == 1)

def fires(b):
    if b.last_col == 5:
        return _mine_below(b) == 0
    return b.ply == 4 and b.last_col == 0

def level(b):
    if b.last_col == 5:
        if _mine_below(b) > 0:
            return 0
        if b.heights[5] == 1:
            return 9 if b.ply <= 12 else 6
        return 3
    if b.ply == 4 and b.last_col == 0:
        return 2
    return 0
