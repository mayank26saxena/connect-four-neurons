def pairs(b):
    # columns 0-3 where my stone is on row 2 with an opponent stone right on top (row 3),
    # next to a column that is still low (height <= 1)
    out = []
    for c in range(4):
        if b.grid[2][c] == 1 and b.grid[3][c] == 2:
            if any(0 <= cc < 7 and b.heights[cc] <= 1 for cc in (c - 1, c + 1)):
                out.append(c)
    return out

def fires(b):
    return len(pairs(b)) >= 1

def level(b):
    p = pairs(b)
    if not p:
        return 0
    n = sum(1 for c in range(4) if b.grid[2][c] == 1 and b.grid[3][c] == 2)
    return min(9, 2 + 2 * n)
