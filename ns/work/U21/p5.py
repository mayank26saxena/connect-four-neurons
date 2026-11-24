def row2_gaps(b):
    # gap cells c (cols 1-3) on row 2 where I hold the other three cells of a horizontal four,
    # and the gap column is still low (height 0 or 1)
    out = []
    g = b.grid
    for c in (1, 2, 3):
        if b.heights[c] > 1:
            continue
        for s in range(max(0, c - 3), min(c, 3) + 1):
            if all(g[2][s + k] == 1 for k in range(4) if s + k != c):
                out.append(c)
                break
    return out

def caps(b):
    # columns 0-4 where my row-2 stone has an opponent stone directly on top of it
    return sum(1 for c in range(5) if b.grid[2][c] == 1 and b.grid[3][c] == 2)

def fires(b):
    return len(row2_gaps(b)) > 0 and caps(b) >= 1

def level(b):
    if not row2_gaps(b):
        return 0
    n = caps(b)
    if n == 0:
        return 2
    return min(9, 3 + 2 * n)
