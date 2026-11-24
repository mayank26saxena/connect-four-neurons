def fires(b):
    if b.ply > 10 or b.last_col != 6:
        return False
    return all(b.grid[r][4] != 1 for r in range(6))

def level(b):
    if fires(b):
        return 9 - max(0, b.ply - 4) // 2
    if b.ply <= 8 and b.last_col in (3, 4, 5, 6):
        return 3
    return 0
