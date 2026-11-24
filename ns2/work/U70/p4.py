def col4_poison(b):
    return b.heights[4] == 0 and (1, 4) in b.their_wins

def best_window(b):
    # most opponent stones in any 4-cell line through (1,4) that has none of my stones
    best = 0
    for dr, dc in ((0, 1), (1, 1), (1, -1), (1, 0)):
        for s in range(4):
            cells = [(1 + (k - s) * dr, 4 + (k - s) * dc) for k in range(4)]
            if not all(0 <= r < 6 and 0 <= c < 7 for r, c in cells):
                continue
            vals = [b.grid[r][c] for r, c in cells]
            if 1 in vals:
                continue
            best = max(best, vals.count(2))
    return best

def fires(b):
    return col4_poison(b)

def level(b):
    if col4_poison(b):
        return 9
    if b.heights[4] == 0 and best_window(b) >= 2:
        return 2
    return 0
