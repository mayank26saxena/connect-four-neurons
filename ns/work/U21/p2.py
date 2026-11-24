def row2_gaps(b):
    # gap cells c (cols 1-3) on row 2 where I have three of a horizontal four and the gap column is not yet filled to row 2
    out = []
    g = b.grid
    for c in (1, 2, 3):
        if b.heights[c] > 1 or g[2][c] != 0:
            continue
        for s in range(max(0, c - 3), min(c, 3) + 1):
            cells = [s + k for k in range(4)]
            if all(g[2][x] == 1 for x in cells if x != c):
                out.append(c)
                break
    return out

def fires(b):
    return len(row2_gaps(b)) > 0

def level(b):
    gs = row2_gaps(b)
    if not gs:
        return 0
    best = 0
    for c in gs:
        s = 4
        for cc in (c - 1, c + 1):
            if 0 <= cc < 7 and b.grid[3][cc] == 2:
                s += 2
        if b.grid[0][4] == 2 or b.grid[1][4] == 2:
            s -= 2
        best = max(best, s)
    return max(1, min(best, 9))
