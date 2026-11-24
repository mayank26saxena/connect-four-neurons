def fires(b):
    c = b.last_col
    if c is None or c not in (0, 5, 6):
        return False
    h = b.heights[c]
    if h < 2 or h > 3:
        return False
    return all(b.grid[r][c] == 2 for r in range(h)) and (h == 3 or c == 5)

def level(b):
    if not fires(b):
        return 0
    c = b.last_col
    if c == 5 and b.heights[5] == 3:
        return 9
    return 6
