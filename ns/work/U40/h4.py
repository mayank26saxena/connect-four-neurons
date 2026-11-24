def opening(b):
    if b.ply != 3:
        return False
    for c in range(7):
        if b.grid[0][c] == 1 and c in (3, 5):
            return False
    return b.heights[5] == 0

CELLS = [((4, 5), 2), ((4, 4), 1), ((5, 5), 2), ((3, 5), 1), ((2, 5), 1),
         ((2, 4), 2), ((1, 1), 1), ((0, 1), 2), ((3, 2), 1)]

def points(b):
    return sum(1 for (r, c), v in CELLS if b.grid[r][c] == v)

def fires(b):
    return opening(b) or points(b) >= 6

def level(b):
    if opening(b):
        return 9
    p = points(b)
    return max(0, min(9, 2 * (p - 3)))
