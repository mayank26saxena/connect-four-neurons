def fires(b):
    if b.heights[5] != 1:
        return False
    cells = [(0, 3), (1, 4), (1, 3), (0, 5)]
    n = sum(1 for (r, c) in cells if b.grid[r][c] == 2)
    return n >= 2

def level(b):
    if b.heights[5] != 1:
        return 0
    cells = [(0, 3), (1, 4), (1, 3), (0, 5)]
    n = sum(1 for (r, c) in cells if b.grid[r][c] == 2)
    return [0, 1, 4, 7, 9][n]
