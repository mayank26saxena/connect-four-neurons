def c3(b, who):
    return sum(1 for r in range(6) if b.grid[r][3] == who)

def fires(b):
    if b.ply == 1:
        return b.last_col in (0, 5, 6)
    mine, theirs = c3(b, 1), c3(b, 2)
    if b.ply >= 4 and mine >= 3 and mine > theirs and b.last_col in (0, 3, 4, 6):
        return True
    if b.ply >= 25 and b.heights[3] <= 1:
        return True
    return False

def level(b):
    if b.ply == 1:
        return {6: 9, 5: 6, 0: 3, 3: 3, 4: 3, 1: 2}.get(b.last_col, 0)
    return 3 if fires(b) else 0
