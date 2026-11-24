def opening(b):
    # ply 3: my single stone not in col 3 or 5, and no opponent stone in col 5
    if b.ply != 3:
        return False
    for c in range(7):
        if b.grid[0][c] == 1 and c in (3, 5):
            return False
    return b.heights[5] == 0

def late(b):
    # opponent stone at row 4 of column 5 (second from top)
    return b.grid[4][5] == 2

def fires(b):
    return opening(b) or late(b)

def level(b):
    if opening(b):
        return 9
    if late(b):
        return 8 if b.grid[4][4] == 1 else 5
    return 0
