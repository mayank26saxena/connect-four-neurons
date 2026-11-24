def bad_cols(b):
    n = sum(1 for c in range(6) if b.heights[c] == 5)
    if b.heights[6] in (2, 3, 4):
        n += 1
    return n

def center_pair(b):
    # opponent owns the two lowest cells of the centre column
    return b.grid[0][3] == 2 and b.grid[1][3] == 2

def fires(b):
    return center_pair(b) and bad_cols(b) == 0

def level(b):
    if bad_cols(b) > 0:
        return 0
    if center_pair(b):
        return 7 if b.ply <= 12 else 4
    return 1
