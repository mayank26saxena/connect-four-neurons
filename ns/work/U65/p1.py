def fires(b):
    if b.ply < 2 or b.heights[1] != 0:
        return False
    opp = sum(1 for c in range(2, 6) if b.grid[0][c] == 2)
    mine = sum(1 for c in range(2, 6) if b.grid[0][c] == 1)
    return opp >= 1 and opp >= mine

def level(b):
    return 6 if fires(b) else 0
