CELLS = [(0, 3), (1, 4), (0, 6), (1, 3), (2, 3), (1, 5), (1, 2)]

def pts(b):
    if b.heights[6] > 2:
        return 0
    return sum(1 for r, c in CELLS if b.grid[r][c] == 2)

def fires(b):
    return pts(b) >= 4

def level(b):
    return [0, 0, 1, 2, 5, 7, 8, 9][pts(b)]
