def runs(b, c):
    # list of (length, lowest_row, highest_row) of vertical runs of opponent stones in column c
    out = []
    r = 0
    h = b.heights[c]
    while r < h:
        if b.grid[r][c] == 2:
            s = r
            while r < h and b.grid[r][c] == 2:
                r += 1
            out.append((r - s, s, r - 1))
        else:
            r += 1
    return out

def fires(b):
    return level(b) >= 4

def level(b):
    h = b.heights[3]
    best = 0
    for k, lo, hi in runs(b, 3):
        top = hi == h - 1
        if top and h < 6:
            if k >= 3:
                v = 9 if lo >= 1 else 4
            elif k == 2:
                v = 5 if lo == 2 else 2
            else:
                v = 0
        else:
            # run capped by my stone (or column full)
            if k >= 3:
                v = 3 if lo >= 1 else 1
                if lo <= 2 and hi >= 4:
                    v = 6
            else:
                v = 0
        best = max(best, v)
    return best
