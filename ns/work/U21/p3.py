def pairs(b):
    # columns 0-3 where my stone sits on row 2 with an opponent stone directly on top of it (row 3)
    return [c for c in range(4) if b.grid[2][c] == 1 and b.grid[3][c] == 2]

def fires(b):
    return len(pairs(b)) >= 1

def level(b):
    n = len(pairs(b))
    return min(9, 3 * n)
