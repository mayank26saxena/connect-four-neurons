def mine_in(b, c):
    return any(b.grid[r][c] == 1 for r in range(6))

def fires(b):
    c = b.last_col
    if c == 1 and not mine_in(b, 1) and b.ply < 20:
        return True
    if c in (0, 2) and b.heights[c] == 1 and b.ply <= 8:
        return True
    return False

def level(b):
    if not fires(b):
        return 0
    if b.last_col == 1:
        if b.heights[1] == 1:
            return 8 if b.ply < 15 else 5
        return 4
    return 4
