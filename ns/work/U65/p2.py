def fires(b):
    # sparse, undeveloped left side, opponent stone(s) low in the centre-right
    if b.ply < 2 or b.ply > 14:
        return False
    if b.heights[1] != 0 or b.heights[0] > 2:
        return False
    opp = 0
    for c in range(2, 7):
        for r in range(2):
            if b.grid[r][c] == 2:
                opp += 1
    mine = 0
    for c in range(2, 7):
        for r in range(2):
            if b.grid[r][c] == 1:
                mine += 1
    return opp >= mine

def level(b):
    if not fires(b):
        return 0
    return max(1, 9 - b.ply // 2)
