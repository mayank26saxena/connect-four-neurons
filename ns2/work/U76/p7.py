def diag_a(b):
    # my stone on (4,3), the cell (3,2) still floating (column 2 has at most 2 stones)
    return b.grid[4][3] == 1 and b.heights[2] <= 2

def diag_b(b):
    # my stones stacked at (1,1),(2,1) on their stone, column 2 at most 1 stone
    g = b.grid
    return b.heights[2] <= 1 and g[2][1] == 1 and g[1][1] == 1 and g[0][1] == 2

def fires(b):
    return diag_a(b) or diag_b(b)

def level(b):
    a = diag_a(b)
    c = diag_b(b)
    if a and c:
        return 9
    if a:
        return 6 if b.heights[4] >= 4 else 4
    if c:
        return 4
    return 0
