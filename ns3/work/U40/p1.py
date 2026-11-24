def fires(b):
    if b.ply > 16:
        return False
    cells = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 2)]
    n = sum(1 for (r, c) in cells if b.grid[r][c] == 2)
    return n >= 3 and b.heights[4] <= 1

def level(b):
    if b.ply > 16:
        return 0
    cells = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 2)]
    n = sum(1 for (r, c) in cells if b.grid[r][c] == 2)
    if b.heights[4] > 1:
        n -= 2
    return max(0, min(9, 2 * n - 2))
