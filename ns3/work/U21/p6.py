def mine_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 1)

def core(b):
    # opponent just dropped a stone in column 2, the centre column is still empty,
    # and none of the stones in column 2 are mine
    return b.last_col == 2 and b.heights[3] == 0 and mine_in(b, 2) == 0

def fires(b):
    return core(b)

def level(b):
    if core(b):
        return 9 if b.ply <= 4 else (8 if b.ply <= 6 else 7)
    L = b.last_col
    if L == 2:
        return 4 if b.heights[3] <= 1 else 3
    if L == 6:
        return 4 if b.heights[6] >= 5 else 2
    if L in (0, 1, 4):
        return 3 if b.ply <= 20 else 2
    return 1
